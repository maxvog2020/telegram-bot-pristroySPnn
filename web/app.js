let tg = window.Telegram.WebApp;

tg.expand();
tg.enableClosingConfirmation()

let main_button = tg.MainButton;
main_button.text = "Опубликовать";
main_button.show();


const COLOR_GREEN = "text-green-500";
const COLOR_RED = "text-red-500";

function toggle(cond, count) {
    if (cond) {
        count.classList.add(COLOR_GREEN);
        count.classList.remove(COLOR_RED);

        main_button.enable();
    } else {
        count.classList.add(COLOR_RED);
        count.classList.remove(COLOR_GREEN);

        main_button.disable();
    }
}


const DEPENDENT_COUNTERS = [
    ['name', 128, true],
    ['address', 128, true],
    ['description', 512, false],
    ['contacts', 128, false],
];

window.onload = () => {
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
    let output = document.getElementById('hidden_output');
    let count = document.getElementById('images_count');
    images.onclick = () => input.click();

    input.onchange = () => {
        let files = input.files;
        let len = files.length;

        count.innerText = `${len}/5`;
        toggle(len <= 5, count);

        output.innerText = files;
    };
};


main_button.onClick(() => {
    tg.sendData({
        name: document.getElementById('name').value,
        address: document.getElementById('address').value,
        description: document.getElementById('description').value,
        contacts: document.getElementById('contacts').value,
        images: document.getElementById('hidden_output').innerText,
    });
});

