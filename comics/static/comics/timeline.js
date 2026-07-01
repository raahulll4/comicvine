let currentIssueId = null;
let currentIsRead = false;

function openModal(issue) {
    currentIssueId = issue.id;
    currentIsRead = issue.is_read;

    document.getElementById('modalNum').textContent = 'Issue #' + issue.num;
    document.getElementById('modalTitle').textContent = (issue.name && issue.name !== '[untitled]') ? issue.name : '';
    document.getElementById('modalDate').textContent = issue.date || 'Unknown';
    document.getElementById('modalCover').src = issue.image || '';
    document.getElementById('modalLink').href = issue.site_url || '#';

    // build the getcomics search url with volume name + issue number
    const searchTerm = encodeURIComponent(issue.volume_name + ' ' + issue.num);
    document.getElementById('modalDownloadLink').href = 'https://getcomics.org/?s=' + searchTerm;

    renderTiein(issue.is_tiein);
    renderArcs(issue.arcs);
    updateReadButton();

    document.getElementById('modalOverlay').classList.add('open');
}

function renderTiein(isTiein) {
    const el = document.getElementById('modalTiein');
    el.innerHTML = isTiein
        ? '<div class="modal-tiein">Tie-in issue</div>'
        : '';
}

function renderArcs(arcs) {
    const arcsEl = document.getElementById('modalArcs');
    const arcsWrap = document.getElementById('modalArcsWrap');

    if (arcs && arcs.length > 0) {
        arcsEl.innerHTML = arcs
            .map(a => `<span class="modal-arc-tag">${a}</span>`)
            .join('');
        arcsWrap.style.display = 'block';
    } else {
        arcsWrap.style.display = 'none';
    }
}

function updateReadButton() {
    const btn = document.getElementById('modalReadBtn');
    if (currentIsRead) {
        btn.className = 'modal-read-btn read';
        btn.innerHTML = '<span class="btn-icon">&#10003;</span> Marked as Read';
    } else {
        btn.className = 'modal-read-btn unread';
        btn.innerHTML = '<span class="btn-icon">&#9675;</span> Mark as Read';
    }
}

function updateCard() {
    const cardImg = document.getElementById('card-img-' + currentIssueId);
    const cardBadge = document.getElementById('card-read-badge-' + currentIssueId);

    if (cardImg) cardImg.classList.toggle('read', currentIsRead);
    if (cardBadge) cardBadge.style.display = currentIsRead ? 'block' : 'none';
}

function toggleRead() {
    const form = document.getElementById('form-' + currentIssueId);
    if (!form) return;

    currentIsRead = !currentIsRead;
    updateReadButton();
    updateCard();
    form.submit();
}

function closeModal(event) {
    if (event.target === document.getElementById('modalOverlay')) {
        closeModalDirect();
    }
}

function closeModalDirect() {
    document.getElementById('modalOverlay').classList.remove('open');
}

document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') closeModalDirect();
});