const { Component, useState, mount, xml, whenReady } = owl;

class App extends Component {
    static template = xml`
    <div class="oe_structure">
        <div class="container">
        <h1 class="iringo_c">Welcome to the House List and their owners</h1>
                    <div class="carmen" t-on-click="pf"><p id="haha" class="clodia">hahha</p><p id = "iringo" class="hihihi"><t t-esc="state.value"/></p></div>
                <h4 class="claudia_b">This is it!!</h4>
                <h4 class="claudia_b">Thank you for your attention!!</h4>
                <h6 class="claudia_b">IRINGO CORA</h6>
                </div>
                </div>`
    x = useState({ value: 'hihihi' });
    state = useState({ value: 2 });
    
    increment() {
        this.state.value++;
        if (this.x.value==='hihihi'){
            this.x.value='iringusa';
            document.getElementById("iringo").className="iringusa";
            document.getElementById("haha").className="clodia2";
            document.body.style.backgroundColor="black";
        }
        else if (this.x.value==='iringusa'){
            this.x.value='hihihi';
            document.getElementById("iringo").className="hihihi";
            document.getElementById("haha").className="clodia";
            document.body.style.backgroundColor="white";
        }
    }
    pf() {
        setInterval(() => this.increment(), 300);
    }
}

whenReady(mount(App, document.body));