// Semua teks dari server dimasukkan dengan textContent, bukan innerHTML.
(() => {
    const app = document.getElementById('award-app');
    const grid = document.getElementById('award-grid');
    const status = document.getElementById('award-status');
    const search = document.getElementById('award-search');
    const csrf = document.querySelector('#award-csrf input').value;
    let timer;
    let controller;

    function element(tag, className, text) {
        const node = document.createElement(tag);
        node.className = className;
        if (text !== undefined) node.textContent = text;
        return node;
    }

    // URL juga harus diperiksa: textContent saja tidak melindungi href/src.
    function safeUrl(value) {
        if (!value) return '';
        try {
            const url = new URL(value, window.location.origin);
            return ['http:', 'https:'].includes(url.protocol) ? url.href : '';
        } catch { return ''; }
    }

    function actionForm(url, label, className) {
        const form = element('form', '');
        form.method = 'post';
        form.action = url;
        const token = element('input', '');
        token.type = 'hidden';
        token.name = 'csrfmiddlewaretoken';
        token.value = csrf;
        const button = element('button', className, label);
        button.type = 'submit';
        form.append(token, button);
        return form;
    }

    function buildCard(award) {
        const card = element('article', 'award-card');
        const certificate = safeUrl(award.certificate_url);
        const thumbnail = safeUrl(award.thumbnail);
        const preview = element(certificate ? 'a' : 'div', 'award-preview');
        if (certificate) {
            preview.href = certificate;
            preview.target = '_blank';
            preview.rel = 'noopener noreferrer';
        }
        if (thumbnail) {
            const img = element('img', '');
            img.src = thumbnail;
            img.alt = `Sertifikat ${award.title}`;
            preview.append(img);
        }
        preview.append(element('span', 'award-file-label', certificate ? 'Open PDF' : 'Award'));
        const body = element('div', 'award-body');
        body.append(element('p', 'award-year', award.year), element('h3', '', award.title), element('p', 'award-issuer', award.issuer));
        const actions = element('div', 'project-actions');
        if (app.dataset.canEdit === 'true') {
            const edit = element('a', 'button', 'Edit');
            edit.href = award.edit_url;
            actions.append(edit);
        }
        if (app.dataset.canDelete === 'true') actions.append(actionForm(award.delete_url, 'Hapus', 'button button-danger'));
        actions.append(actionForm(award.like_url, `${award.is_liked ? 'Unlike' : 'Like'} (${award.like_count})`, `button button-star${award.is_liked ? ' is-starred' : ''}`));
        body.append(actions);
        card.append(preview, body);
        return card;
    }

    // GET: baca JSON, kemudian ubah DOM agar daftar muncul tanpa reload.
    async function loadAwards() {
        if (controller) controller.abort();
        const current = new AbortController();
        controller = current;
        grid.replaceChildren();
        status.hidden = false;
        status.textContent = 'Memuat penghargaan…';
        try {
            const url = new URL(app.dataset.endpoint, window.location.origin);
            url.searchParams.set('q', search.value.trim());
            const response = await fetch(url, {signal: current.signal});
            if (!response.ok) throw new Error('Gagal memuat data');
            const data = await response.json();
            if (current.signal.aborted) return;
            grid.replaceChildren(...data.awards.map(buildCard));
            status.textContent = search.value.trim() ? 'Tidak ada penghargaan yang cocok.' : 'Belum ada penghargaan yang ditambahkan.';
            status.hidden = data.awards.length > 0;
        } catch (error) {
            if (error.name === 'AbortError') return;
            status.textContent = 'Gagal memuat penghargaan. Silakan coba lagi.';
        }
    }

    // Debounce: batalkan timer lama, tunggu 350 ms setelah input terakhir.
    search.addEventListener('input', () => {
        clearTimeout(timer);
        if (controller) controller.abort();
        timer = setTimeout(loadAwards, 350);
    });
    document.getElementById('award-search-form').addEventListener('submit', event => {
        event.preventDefault();
        clearTimeout(timer);
        loadAwards();
    });

    // Modal tidak dirender untuk pengunjung/editor, jadi periksa form dulu.
    const form = document.getElementById('award-form');
    if (form) form.addEventListener('submit', async event => {
        event.preventDefault(); // Hentikan pengiriman form biasa yang memuat ulang halaman.
        const button = form.querySelector('[type="submit"]');
        const errors = document.getElementById('award-form-errors');
        button.disabled = true;
        errors.textContent = '';
        try {
            // FormData menyertakan csrfmiddlewaretoken dari {% csrf_token %}.
            const response = await fetch(form.action, {method: 'POST', body: new FormData(form)});
            const result = await response.json().catch(() => ({}));
            if (!response.ok) {
                const messages = result.errors ? Object.values(result.errors).flat().map(error => error.message) : [result.message || `Permintaan gagal (${response.status}).`];
                throw new Error(messages.join(' '));
            }
            form.reset();
            document.getElementById('add-award-modal').hidePopover();
            showToast('Berhasil', result.message, 'success');
            search.value = '';
            clearTimeout(timer);
            await loadAwards();
        } catch (error) {
            errors.textContent = error.message;
            showToast('Gagal menambahkan penghargaan', error.message, 'error');
        } finally { button.disabled = false; }
    });
    loadAwards();
})();
