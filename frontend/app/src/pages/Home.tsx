import "./Home.css";
function Home() {
  return (
    <div>
      <div className="Header">
        <div>
          <h1>Welcome to Halijams</h1>
        </div>
      </div>
      <div className="rants">
        <p>Rants to Resolution</p>
      </div>
      <div>
        <a href="/map">Rants</a>
      </div>
    </div>
  );
}

export default Home;
