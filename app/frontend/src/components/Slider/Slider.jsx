import React from 'react';
import styles from './Slider.module.css'

export const Slider = ({arr}) => {
    let index = 1;
    let indexX = 2;
    let indexY = 3;
    
    const next = () => {
        let slides = document.getElementsByName('slide')
        const activeSlide = (n, x, y) => {
            slides.forEach(slide => {
                slide.classList.remove('active')
                slide.style.display = "none"
            }) 
            slides[n].style.display = "block"
            slides[x].style.display = "block"
            slides[y].style.display = "block"
            // slides[n-1].classList.add('active')
            // slides[n+1].classList.add('active')
    }
    if(index === slides.length - 1){
        indexX = 0
        activeSlide(index, indexX, indexY);
        index = 0
        indexX++
        indexY++
        console.log('сценарий:', 1)
      } else {
          if(index === slides.length - 2){
            indexY = 0
            activeSlide(index, indexX, indexY);
            index++;
            indexX++;
            indexY++;
            console.log('сценарий:', 2)
          }else{
            activeSlide(index, indexX, indexY);
            index++;
            indexX++;
            indexY++;
            console.log('сценарий:', 3)
          }
      }
}
    return (
        <>
            <div className={styles.wrapper}>
            <img alt="next" src="/images/PolygonPrev.png" onClick={next} className={styles.prevButton} height="42px" width="42px"></img>
                <div className={styles.wrapperSlider}>
                    {
                        arr.map((item) => (
                            <div className={styles.slide} name={'slide'} key={item}>
                                <img src={item} alt='slide' width="200px" height="130px"></img>
                            </div>
                        ))
                    }
                </div>
                <img alt="next" src="/images/PolygonNext.png" onClick={next} className={styles.nextButton} height="42px" width="42px"></img>
            </div>
        </>
    )
}