import { GamePage, GameHeader, GameContent, GameButton } from '../../components'; // Adicionei o GameButton
import styles from "./Home.module.css";
import logo from '../../assets/images/trocadu.png';

const Home: React.FC = () => {
  return (
    <GamePage className={styles.homePage}>
      <GameHeader>
        
      </GameHeader>
      
      <GameContent fullscreen>
        <div className={styles.menuContainer}>
          <img src={logo} alt="Trocadu Icon" className={styles.logo} />
          
          <div>
            <GameButton routerLink="/select-mode" variant="primary">
              Jogar
            </GameButton>
            <GameButton routerLink="/my-account" variant="primary">
              Minha Conta
            </GameButton>
            <GameButton routerLink="/word-packs" variant="primary">
              Pacotes de Palavas
            </GameButton>
          </div>
          
        </div>
      </GameContent>
    </GamePage>
  );
};

export default Home;