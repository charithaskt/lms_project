import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = { 
       biblios: []
    };
  }
/*
fetch('URL_GOES_HERE', { 
   method: 'post', 
   headers: new Headers({
     'Authorization': 'Basic '+btoa('username:password'), 
     'Content-Type': 'application/x-www-form-urlencoded'
   }), 
   body: 'A=1&B=2'
 });
*/

  async componentDidMount() {
    try {
      //const res = await fetch('http://127.0.0.1:8000/api/v1/biblios/?format=json');
    const res = await fetch('http://127.0.0.1:8000/api/v1/biblios/?format=json',    { 
                    method: 'get', 
                    headers: new Headers({
                    'Authorization': 'Basic '+btoa('charitha.tsk@gmail.com:admin123'), 
                    'Content-Type': 'application/x-www-form-urlencoded'
                    }), 
    });

      const biblios = await res.json();
      this.setState({
        biblios
      });
    } catch (e) {
      console.log(e);
    }
  }

  render() {
    return (
     <div>
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <p>
            Edit <code>src/App.js</code> and save to reload.
          </p>
          <a
            className="App-link"
            href="https://reactjs.org"
            target="_blank"
            rel="noopener noreferrer"
          >
            Learn React
          </a>
        </header>
       </div>
       <div> 
        {this.state.biblios.map(item => (
          <div key={item.biblionumber}>
            <p class="indent-10"><strong><a href={"http://localhost:8000/api/v1/biblio/" + item.biblionumber } target="blank">{item.title}</a></strong></p>
            <p class="indent-10">{item.callnumber}</p>
            <p class="indent-10">{item.edition}</p>
            <p class="indent-10">{item.copyrightdate}</p>
            <p class="indent-10">{item.pages}</p>
            <p class="indent-10">{item.itemtype}</p>
          </div>
        ))}
       </div>
     </div>
    );
  }
}

export default App;
