import React from 'react';
import { IonButton } from '@ionic/react';
import styles from './GameButton.module.css';

type GameButtonProps = React.ComponentProps<typeof IonButton> & {
  variant?: 'primary' | 'secondary' | 'accent';
};

const GameButton: React.FC<GameButtonProps> = ({ 
  children, 
  className, 
  variant = 'primary',
  ...rest 
}) => {
  return (
    <IonButton
      className={`${styles.gameButton} ${styles[variant]} ${className || ''}`}
      expand="block"
      shape="round"
      {...rest}
    >
      {children}
    </IonButton>
  );
};

export default GameButton;