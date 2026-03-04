const btn = document.getElementById('randomBtn');
const resultDiv = document.getElementById('result');

async function fetchRandom() {
    const resp = await fetch('/random');
    if (!resp.ok) throw new Error('Failed');
    return resp.json();
}

async function fetchSimilar(id) {
    const resp = await fetch(`/similar/${id}`);
    if (!resp.ok) throw new Error('Failed');
    return resp.json();
}

function createLink(item) {
    const a = document.createElement('a');
    a.href = item.url;
    a.target = '_blank';
    a.textContent = item.title;
    return a;
}

btn.addEventListener('click', async () => {
    resultDiv.innerHTML = '';
    try {
        const random = await fetchRandom();

        const articleDiv = document.createElement('div');
        articleDiv.className = 'article';
        articleDiv.appendChild(createLink(random));
        resultDiv.appendChild(articleDiv);

        const pre = document.createElement('div');
        pre.className = 'preloader';
        pre.textContent = 'Поиск 5 наиболее похожих статей…';
        resultDiv.appendChild(pre);

        const similar = await fetchSimilar(random.id);
        pre.remove();

        similar.forEach(item => {
            const div = document.createElement('div');
            div.className = 'similar';
            div.appendChild(createLink(item));
            resultDiv.appendChild(div);
        });
    } catch (e) {
        const err = document.createElement('div');
        err.style.color = 'red';
        err.textContent = 'Произошла ошибка. Пожалуйста, попробуйте ещё раз.';
        resultDiv.appendChild(err);
        console.error(e);
    }
});