import './App.css';
import Header from './components/Header';
import Fullness from './components/Fullness';

function App() {
  return (
    <>
     <Header name1="Automated Recycling Containers Monitoring" name2={["Cisco Meraki Global Hackathon 2022"]}/>
     <p></p>
     <Fullness name="Cam Meraki MV Sens - Q2JV-4QEU-G7X6"/>
    </>
  );
}

export default App;
