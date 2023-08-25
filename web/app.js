let tg = window.Telegram.WebApp;
let main_button = tg.MainButton;

let files = [];
let reader = new FileReader();


const COLOR_GREEN = "text-green-500";
const COLOR_RED = "text-red-500";
const DEPENDENT_COUNTERS = [
    ['name', 128, true],
    ['address', 128, true],
    ['description', 512, false],
    ['contacts', 128, false],
];


function toggleBlock() {
    let reds = document.getElementsByClassName(COLOR_RED);
    if (reds.length > 0) {
        main_button.disable();
    } else {
        main_button.enable();
    }
}

function toggle(cond, count) {
    if (cond) {
        count.classList.add(COLOR_GREEN);
        count.classList.remove(COLOR_RED); 
    } else {
        count.classList.add(COLOR_RED);
        count.classList.remove(COLOR_GREEN);
    }

    toggleBlock();
}


window.onload = () => {
    tg.expand();
    tg.enableClosingConfirmation()

    main_button.text = "Опубликовать";
    main_button.show();
    toggleBlock();

    DEPENDENT_COUNTERS.forEach(item => {
        let [name, max_len, req] = item;

        let tag = document.getElementById(name);
        let count = document.getElementById(`${name}_count`);

        let oninput = () => {
            let len = tag.value.length;
            count.innerText = `${len}/${max_len}`;

            let cond = len <= max_len
            if (req) { cond = cond && len > 0; }

            toggle(cond, count);
        };

        oninput();
        tag.oninput = oninput;
    });

    let images = document.getElementById('images');
    let input = document.getElementById('hidden_input');
    let count = document.getElementById('images_count');
    
    images.onclick = () => input.click();

    setInterval(() => {
        files = input.files;
        let len = files.length;

        count.innerText = `(${len}/5)`;
        toggle(len <= 5, count);
    }, 50);


    main_button.onClick(() => {
        let data = {
            name: document.getElementById('name').value,
            address: document.getElementById('address').value,
            description: document.getElementById('description').value,
            contacts: document.getElementById('contacts').value,
            image_count: document.getElementById('image_count').value,
            telegram: document.getElementById('telegram').checked,
        };
 
        tg.sendData(JSON.stringify(data));
    });
};

