import "./Home.css";
import bubbleguy from "../assets/We’re ranting to a resolution.png";
// import backdrop from "../assets/backdrop.png";
// import speaker from "../assets/peaker.png";

function Home() {
  return (
    <div>
      {/* <img className="backdrop" src={backdrop} alt="" /> */}
      <div className="Header">
        <div>
          <h1>Lets rant about it!</h1>
        </div>
      </div>
      <div className="bubble">
        <span>
          <img className="chatbubble" src={bubbleguy} alt="chat bubble"></img>
          <p>Ranting to a resolution!</p>
        </span>
      </div>
      <div className="rants-btn">
        <a href="/map">Get Started</a>
      </div>
      <div className="home"></div>
      {/* <div className="speaker">
        <img
          className="background_speaker"
          src={speaker}
          alt="speakerphone"
        ></img>
      </div> */}
    </div>
  );
}

export default Home;
