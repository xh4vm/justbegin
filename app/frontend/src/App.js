// import {Header} from './components/Header/Header';
// import { WelcomeBanner } from './components/Banners/WelcomeBanner';
// import { ContentBlock, Footer, NavigationPanel } from './components';
import React from 'react';
import { Route, Switch } from 'react-router';
import { WelcomePage } from './Pages/WelcomePage/WelcomePage';
import { Autorization } from './Pages/Autorization/Autorization'
// const myArr = ['Arts','Comics & ilustration', 'Design & Tech', 'Film', 'Food & Craft', 'Games', 'Music', 'Publishing']

function App() {
  
  return (
    <>
            <Switch>
                <Route
                    exact
                    path="/"
                    render={() =>
                        (
                           <WelcomePage/>
                        )}
                />
                <Route
                    exact
                    path="/biba"
                    render={() =>
                        (
                           <Autorization/>
                        )}
                />
            </Switch>
        </>
    // <div className="App">
    //     <Header></Header>
    //     <WelcomeBanner></WelcomeBanner>
    //     <NavigationPanel arr={myArr}></NavigationPanel>
    //     <ContentBlock></ContentBlock>
    //     <Footer></Footer>
    // </div>
  );
}

export default App;
