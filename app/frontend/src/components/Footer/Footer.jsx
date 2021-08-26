import React from 'react';
import styles from './Footer.module.css';


export const Footer = () => {
    return(
        <>
            <footer className={styles.footer}>
                <ul className={styles.footerList}>
                    <li className={styles.footerListItem}><a><img alt="facebook" src="/images/faceBook.png"></img></a></li>
                    <li className={styles.footerListItem}><a><img alt="home" src="/images/home.png"></img></a></li>
                    <li className={styles.footerListItem}><a><img alt="instagramm" src="/images/instagramm.png"></img></a></li>
                </ul>
            </footer>
        </>
    )
}