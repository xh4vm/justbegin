import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import styles from './Header.module.css'

const scrollHandler = (e) => {
    if (e.target.documentElement.scrollHeight - (e.target.documentElement.scrollTop + window.innerHeight) < 900) {
       let aa = document.getElementById('headerHeader')
       aa.classList.add(`${styles.active}`)
    } else {
        let aa = document.getElementById('headerHeader')
        aa.classList.remove(`${styles.active}`)
    }
  }

export const Header = () => {
    useEffect(()=>{
        document.addEventListener('scroll', scrollHandler)
        return function () {
          document.removeEventListener('scroll', scrollHandler)
        }
      }, [])
    return (
        <>
            <header className={styles.header} id="headerHeader">
                <div className={styles.headerWrapper}>
                    <aside>
                        <img src="/images/bebeshka.png" alt="bebeshka" className={styles.headerPic}></img>
                    </aside>
                    <nav className={styles.navBar}>
                        <span className={styles.myHeaderLink}>Главная</span>
                        <span className={styles.myHeaderLink}>О нас</span>
                        <span className={styles.myHeaderLink}>Проекты</span>
                        <Link to={'/biba'} className={styles.Link}><span className={styles.myHeaderLink}>Войти</span></Link>
                    </nav>
                </div>
            </header>
        </>
    )
}