import React, { useEffect } from 'react';
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
    const ent = () => {
        document.querySelector('#modal').classList.add(`${styles.activeModal}`)
        document.querySelector('#MyAutorizationWrapper').classList.add(`${styles.MyAutorizationWrapper}`)
    }
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
                        <span onClick={ent} className={styles.myHeaderLink}>Войти</span>
                    </nav>
                </div>
            </header>
        </>
    )
}