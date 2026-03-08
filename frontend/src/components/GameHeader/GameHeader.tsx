import React from 'react';
import { IonHeader } from '@ionic/react';
import styles from './GameHeader.module.css';

type GameHeaderProps = React.ComponentProps<typeof IonHeader>;

function GameHeader({ children, className, ...rest }: GameHeaderProps) {
  return (
    <IonHeader 
      className={`${styles.gameHeader} ${className || ''}`} 
      {...rest}
    >
        { children }
    </IonHeader>
  );
}

export default GameHeader;