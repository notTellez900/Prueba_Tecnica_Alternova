let table;
let token;
const login = async() =>{
    try {
        const url = 'http://127.0.0.1:8000/users/login';
        const dataBody = {
            email: 'nicolas@gmail.com',
            password: 'venus12*'
        }
        const response = await fetch(url, {
            method: 'post',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dataBody)
        });

        const data = await response.json();

        newToken = data.result['token'];

        token = newToken;
        
    } catch (error) {
        console.log(error);
    }
}

const listStreamings = async (filterValue) =>{
    try {
        const url = filterValue ? `./getStreamings/${filterValue}` : './getStreamings';
        const response = await fetch(url, {
            method: 'get',
            headers: {
                'Authorization': `Token ${token}`,
                'Content-Type': 'application/json'
            }
        });

        const data = await response.json();

        if(data.message == "success"){
            const cuerpo = document.getElementById('cuerpo');
            const table = document.getElementById('tableStreamings');
    
            // Borra la tabla anterior si existe
            if (table) {
                table.remove();
            }
            
            // Crear tabla nueva
            const newTable = document.createElement('table');
            newTable.id = 'tableStreamings';
            newTable.classList.add('table', 'table-striped', 'mt-4')

            // Crear encabezado de tabla
            const thead = document.createElement('thead');
            thead.innerHTML = `
            <tr>
                <th>Name</th>
                <th>Genres</th>
                <th>Type</th>
                <th>Rating</th>
            </tr>
            `;

            newTable.appendChild(thead);
            // Crea la nueva tabla y agrega las filas
           
            const tbody = document.createElement("tbody");
            
            const rows = data['result'].map( element =>{
                const row = document.createElement('tr');
                row.innerHTML = `
                <td>${element.name}</td>
                <td>${element.gender}</td>
                <td>${element.stream_type}</td>
                <td>${element.average_rating}</td>
                `;
                return row;
            });
            
            tbody.append(...rows);
            newTable.appendChild(tbody);
            //const tbody = table.querySelector("tbody");
            cuerpo.appendChild(newTable);
            
        }
        console.log(data)   
    } catch (error) {
        console.log(error)
    }
}



const getRandStreaming = async () =>{
    try {
        const response = await fetch('./getRandomStreaming', {
            method: 'get',
            headers: {
                'Authorization': `Token ${token}`,
                'Content-Type': 'application/json'
            }
        });

        const data = await response.json();

        if(data.message == "success"){
            let cuerpo = document.getElementById('randBody') ;
        
            const card = document.createElement('div');
            card.classList.add('card','mt-4');
            
            const cardBody = document.createElement('div');
            cardBody.classList.add('card-body');
            
            const cardTitle = document.createElement('h5');
            cardTitle.classList.add('card-title');
            cardTitle.textContent = data.result.name;
            
            const cardText = document.createElement('p');
            cardText.classList.add('card-text');
            cardText.innerHTML = `Genres: ${data.result.gender}<br>Type: ${data.result.stream_type}<br>Visualizations: ${data.result.num_visualizations}<br>Rating: ${data.result.average_rating}`;
            
            cardBody.appendChild(cardTitle);
            cardBody.appendChild(cardText);
            card.appendChild(cardBody);
            
            cuerpo.appendChild(card);
        }
        const { result } = data; 
        const id = result.id;
        return id;   

    } catch (error) {
        console.log(error)
    }
}

const watchStreaming = async (idStreaming)=> {
    try {
        const response = fetch(`./markAsSeen/${idStreaming}`, {
            method: 'put',
            headers: {
                'Authorization': `Token ${token}`,
                'Content-Type': 'application/json'
            }
        });

        return response;

    } catch (error) {
        console.log(error);
    }
}

const rateStreaming = async (idStreaming, value) => {

    const data = {
        rating: value
    }

    try {
        const response = fetch(`./rateStreaming/${idStreaming}`, {
            method: 'put',
            headers: {
                'Authorization': `Token ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        return response;

    } catch (error) {
        console.log(error);
    }
}


const alertPlaceholder = document.getElementById('alertPlaceholder');

const appendAlert = (message, type) =>{
    const wrapper = document.createElement('div');
    wrapper.innerHTML = [
        `<div class="alert alert-${type} alert-dismissible" role="alert">`,
        `<div>${message}</div>`,
        `<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>`,
        `</div>`
    ].join('')

    alertPlaceholder.append(wrapper)
}

const inicio = async () => {
    await listStreamings();

    const item = getRandStreaming();

    btnSeen.addEventListener('click', (e) =>{
        let idItem;
        item.then( resultado =>{
            console.log(resultado)
            idItem = resultado;
            let message = watchStreaming(idItem);
            message.then(result =>{
                if(result.statusText == 'Bad Request'){
                    appendAlert("You've already seen this streaming", "danger");
                }else{
                    appendAlert("The streaming has been marked as a view", "success");

                }
            });
        });
    });

    btnRating.addEventListener('click', (e) =>{
        const value = document.getElementById('rating').value;
        let idItem;
        item.then( resultado =>{
            idItem = resultado;
            let message = rateStreaming(idItem, value);
            message.then( result => {
                if(result.statusText == 'Bad Request'){
                    appendAlert("You've already rated this streaming", "danger");
                }else{
                    appendAlert("You have rated this movie successfully", "success");
                }
            });
        });
        console.log(value);
    });
    
   

    orderSelect.addEventListener('change', (e) =>{
        if (table) {
            const rows = table.querySelectorAll("tr");
            rows.forEach((row) => row.remove());
        }
        listStreamings(e.target.value);
    });
    
    search.addEventListener('click', (e) =>{
        const value = document.getElementById('textSearch').value;
        if (table) {
            const rows = table.querySelectorAll("tr");
            rows.forEach((row) => row.remove());
        }
        listStreamings(value);
    })
}

window.addEventListener('load', async () =>{
    await login();
    await inicio();
})