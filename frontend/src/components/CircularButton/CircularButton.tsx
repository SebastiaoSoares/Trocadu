import React from 'react';
import { IonButton, IonIcon } from '@ionic/react';
import styles from './CircularButton.module.css';

type CircularButtonProps = React.ComponentProps<typeof IonButton> & {
  variant?: 'primary' | 'secondary' | 'accent';
  icon?: string;
};

const CircularButton: React.FC<CircularButtonProps> = ({ 
  className, 
  variant = 'primary',
  icon = 'heart',
  ...rest 
}) => {
  return (
    <IonButton
      className={`${styles.circularButton} ${styles[variant]} ${className || ''}`}
      expand="block"
      shape="round"
      {...rest}
    >
        <IonIcon slot="icon-only" icon={icon}></IonIcon>
    </IonButton>
  );
};

export default CircularButton;