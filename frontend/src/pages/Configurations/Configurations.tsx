import { GameContent, GamePage } from '../../components';

import styles from "./Configurations.module.css";
import logo from '../../assets/images/trocadu.png';

const Configurations: React.FC = () => {
  return (
    <GamePage>
      <GameContent fullscreen>
        <div className={styles.menuContainer}>
          <img src={logo} alt="Trocadu Icon" className={styles.logo} />
        </div>
      </GameContent>
    </GamePage>
  );
};

export default Configurations;
