"""Módulo contendo o caso de uso principal do modo Competitivo Clássico."""

from src.domain.entities.placar import Placar
from src.domain.registry.partida_registry import PartidaRegistry
from src.domain.interfaces.partida_base import GerenciadorDePartida
from src.domain.shared.mixins import PermutadorMixin
from src.domain.entities.configuracao import ConfiguracaoDePartida
from typing import Any, Dict, Optional
from src.infrastructure.database.database import SessionLocal
from src.infrastructure.repositories.partida_repository import PartidaRepository

@PartidaRegistry.registrar("COMPETITIVA_CLASSICA")
class PartidaCompetitivaClassica(PermutadorMixin, GerenciadorDePartida):
    """Orquestra as regras específicas de uma partida no modo competitivo clássico.

    Esta classe gere o rodízio de duplas (ida e volta), a contagem de pontos acumulada
    e o processamento final para determinar o campeão e guardar o histórico no
    banco de dados.

    Attributes:
        _ranking (Dict[str, int]): Dicionário interno que mapeia o nome de cada 
            jogador à sua pontuação total.
        _dupla_atual (Equipe | None): A dupla de jogadores que está a jogar a rodada atual.
        _fase_rodada (str | None): Indica se a dupla está na fase de "ida" 
            (primeiro jogador como guia) ou "volta" (papéis invertidos).
    """

    def __init__(self, pool_jogadores: list, pacote_palavras: object, configuracao: Optional[ConfiguracaoDePartida] = None):
        """Inicializa o gestor da partida competitiva.

        Args:
            pool_jogadores (list): Lista de instâncias de `Jogador` participantes.
            pacote_palavras (object): A fonte de palavras instanciada para o jogo.
            configuracao (ConfiguracaoDePartida, optional): Configurações de limites 
                de tempo e palavras. Se não fornecida, usa os padrões.
        """
        super().__init__(pool_jogadores, pacote_palavras, configuracao)
        self._ranking: Dict[str, int] = {}
        self._dupla_atual = None
        self._fase_rodada = None

    def _setup(self) -> None:
        """Realiza as configurações iniciais antes de a partida começar.

        Gera todas as permutações de duplas necessárias utilizando o mixin 
        `PermutadorMixin` e inicializa o ranking de todos os jogadores com zero pontos.
        """
        self._fila_de_duplas = self._gerar_permutacoes_duplas()
        self._ranking = {jogador.nome: 0 for jogador in self._pool_jogadores}

    def computar_pontos_rodada(self, pontos_conquistados: int) -> Dict[str, Any]:
        """Adiciona os pontos obtidos no turno ao ranking global da dupla atual.

        Args:
            pontos_conquistados (int): Os pontos a serem adicionados aos dois 
                jogadores da dupla atual.

        Returns:
            Dict[str, Any]: Um dicionário com uma mensagem de sucesso e o 
            estado atualizado do ranking global.

        Raises:
            ValueError: Se o método for chamado quando não há nenhuma rodada/turno ativo.
        """
        if not self._turno_atual or not self._turno_atual.dupla:
            raise ValueError("Não há rodada ativa para pontuar.")

        nome_j1 = self._turno_atual.dupla.jogador_1.nome
        nome_j2 = self._turno_atual.dupla.jogador_2.nome

        if nome_j1 in self._ranking:
            self._ranking[nome_j1] += pontos_conquistados
        
        if nome_j2 in self._ranking:
            self._ranking[nome_j2] += pontos_conquistados

        return {
            "mensagem": f"Pontos computados: +{pontos_conquistados} para {nome_j1} e {nome_j2}",
            "ranking_atual": self._ranking
        }

    def avancar(self) -> Dict[str, Any]:
        """Avança a partida para a próxima rodada ou fase (ida/volta).

        Controla a máquina de estados do jogo. Se uma nova dupla assumir, 
        inicia a fase de "ida". Se a dupla já jogou a ida, inverte os papéis 
        para a fase de "volta". Se a fila de duplas estiver vazia, finaliza o jogo.

        Returns:
            Dict[str, Any]: O estado da nova rodada (com fase, dupla, palavra e tempo)
            ou o resultado final (status "FINALIZADO" e dados do campeão) caso o jogo acabe.
            Retorna uma mensagem de erro se a partida não estiver `EM_ANDAMENTO`.
        """
        if self._status != self.Status.EM_ANDAMENTO:
             return {"erro": "A partida precisa ser iniciada antes de avançar."}

        if self._dupla_atual is None or self._fase_rodada == "volta":
            if not self._fila_de_duplas:
                self._status = self.Status.FINALIZADO
                resultado_final = self._processar_vitoria()
                return {
                    "status": "FINALIZADO",
                    "dados": resultado_final
                }

            self._dupla_atual = self._fila_de_duplas.popleft()
            self._fase_rodada = "ida"
            self._executar_rodada_ida_e_volta(self._dupla_atual)
            
        else:
            self._fase_rodada = "volta"
            self._executar_rodada_ida_e_volta(self._dupla_atual)
            
            self._turno_atual.trocar_funcoes()

        return {
            "status": "RODADA_NOVA",
            "fase": self._fase_rodada,
            "dupla": {
                "guia": self._turno_atual.guia_atual.nome,
                "adivinhador": self._turno_atual.adivinhador_atual.nome
            },
            "palavra": self._turno_atual.palavra_atual,
            "tempo_limite": self._turno_atual.tempo_limite,
            "palavras_disponiveis": self._turno_atual.palavras_disponiveis
        }

    def _processar_vitoria(self) -> Dict[str, Any]:
        """Calcula o resultado final, salva o histórico e exibe o encerramento.

        Utiliza a entidade `Placar` para processar e ordenar o ranking, descobre 
        o campeão, e persiste os dados na base de dados utilizando o padrão Repository.

        Returns:
            Dict[str, Any]: Um dicionário contendo a mensagem de encerramento, 
            os dados do campeão isolado e a tabela completa de classificação.
        """
        self._status = self.Status.FINALIZADO
        ranking_formatado = Placar.processar_ranking(self._ranking)
        campeao = Placar.obter_campeao(ranking_formatado)

        db = SessionLocal()
        try:
            repo = PartidaRepository(db)
            repo.salvar_historico("COMPETITIVA_CLASSICA", ranking_formatado)
        finally:
            db.close()

        return {
            "mensagem": "Torneio encerrado!",
            "campeao": campeao,
            "ranking_completo": ranking_formatado
        }