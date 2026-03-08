import React from 'react';
import { IonContent } from '@ionic/react';
import styles from './GameContent.module.css';

type GameContentProps = React.ComponentProps<typeof IonContent>;

function GameContent({ children, className, ...rest }: GameContentProps) {
  return (
    <IonContent 
      className={`${styles.GameContent} ${className || ''}`} 
      {...rest}
    >
        { children }
    </IonContent>
  );
}

export default GameContent;