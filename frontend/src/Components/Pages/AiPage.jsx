import AIChat from "../AiBot/AiBot";
import HeroSection from "../AiBotHero/AiBotHero";
import Header from "../Header/Header"

function AiPage(){
    return(
        <div>
            <Header/>
            <HeroSection/>
            <AIChat/>
        </div>
    )
}

export default AiPage;