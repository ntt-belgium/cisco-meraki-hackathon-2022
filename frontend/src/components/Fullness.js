import React, { useState, useEffect } from "react";
import axios from 'axios';

function Fullness(props) {
    const [level, setLevel] = useState(0);
    const [n_persons, setPersons] = useState(0);

    useEffect(() => {
      const interval = setInterval(() => {
        axios.get(`http://localhost:5000`)
        .then(res => {
          setLevel(res.data.fullness);
          setPersons(res.data.n_persons);
        })
      }, 400);
      return () => clearInterval(interval)
    }, [] );
  
    const image_name = "container_"+(level*25)+".png"
    const divstyle = { marginLeft: '200px' }    
    return (<div style={divstyle}>
        <table>
            <tbody>
        <tr>
          <td>
            <div>{props.name}</div>  
            <p></p>
            <img src={image_name} alt={"level "+level}/>
            <p><h2>Persons: {n_persons}</h2></p>
         </td>
        </tr>
        </tbody>
    </table></div>);
}

export default Fullness;
