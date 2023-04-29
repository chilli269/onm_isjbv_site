
const { Component, useState, mount, xml } = owl;

class Greeter extends Component {
    static template = "Greeter";
    
    setup() {
        this.state = useState({ word: 'Hello', name: "World" });
    }

    toggle() {
        this.state.word = this.state.word === 'Hi' ? 'Hello' : 'Hi';
    }
}


mount(Greeter, document.body, { templates: "testing2.first_template" });