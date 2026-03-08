import React from 'react';
import { IonPage } from '@ionic/react';
import styles from './GamePage.module.css';

type GamePageProps = React.ComponentProps<typeof IonPage>;

function GamePage({ children, className, ...rest }: GamePageProps) {
  return (
    <IonPage 
      className={`${styles.gamePage} ${className || ''}`} 
      {...rest}
    >
        { children }
    </IonPage>
  );
}

export default GamePage;