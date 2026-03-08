import { GameContent, GamePage } from '../../components';

import styles from "./SelectMode.module.css";
import logo from '../../assets/images/trocadu.png';

const SelectMode: React.FC = () => {
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

export default SelectMode;
