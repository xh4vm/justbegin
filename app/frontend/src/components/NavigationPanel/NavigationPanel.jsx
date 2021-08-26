import React from 'react';
import styles from './NavigationPanel.module.css'

export const NavigationPanel = ({arr}) => {
    return (
        <>
        <div className={styles.navBlock}>
            <div className={styles.myLinkWrapper}>
                <nav className={styles.navWrapp}>
                    {
                     arr.map((item) => (
                         <a href="#" className={styles.myLink} key={item}>{item}</a>
                        ))
                 }
                </nav>
            </div>
        </div>
        </>
    )
}