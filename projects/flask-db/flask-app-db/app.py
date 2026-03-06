from flask import Flask, request, jsonify, render_template_string
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

with app.app_context():
    db.create_all()

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>User Manager 🚀</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    font-family: 'Inter', sans-serif;
    background: #0f0f13;
    color: #e2e8f0;
    min-height: 100vh;
    padding: 40px 20px;
  }

  .container {
    max-width: 640px;
    margin: 0 auto;
  }

  /* Header */
  .header {
    text-align: center;
    margin-bottom: 40px;
  }
  .header .badge {
    display: inline-block;
    background: rgba(99,102,241,0.15);
    border: 1px solid rgba(99,102,241,0.3);
    color: #a5b4fc;
    font-size: 0.75rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 5px 14px;
    border-radius: 20px;
    margin-bottom: 16px;
  }
  .header h1 {
    font-size: 2.2rem;
    font-weight: 600;
    color: #f1f5f9;
    margin-bottom: 8px;
  }
  .header p {
    color: #64748b;
    font-size: 0.95rem;
  }

  /* Stats */
  .stats {
    display: flex;
    gap: 12px;
    margin-bottom: 28px;
  }
  .stat-card {
    flex: 1;
    background: #1a1a24;
    border: 1px solid #2a2a38;
    border-radius: 14px;
    padding: 18px;
    text-align: center;
  }
  .stat-num {
    font-size: 2rem;
    font-weight: 600;
    color: #818cf8;
    display: block;
  }
  .stat-label {
    font-size: 0.75rem;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 4px;
  }

  /* Card */
  .card {
    background: #1a1a24;
    border: 1px solid #2a2a38;
    border-radius: 18px;
    padding: 28px;
    margin-bottom: 20px;
  }
  .card-title {
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #475569;
    margin-bottom: 18px;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .card-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #2a2a38;
  }

  /* Form */
  .input-row {
    display: flex;
    gap: 10px;
  }
  input[type="text"] {
    flex: 1;
    background: #0f0f13;
    border: 1px solid #2a2a38;
    border-radius: 10px;
    padding: 12px 16px;
    color: #e2e8f0;
    font-size: 0.95rem;
    font-family: 'Inter', sans-serif;
    outline: none;
    transition: border-color 0.2s;
  }
  input[type="text"]:focus { border-color: #6366f1; }
  input[type="text"]::placeholder { color: #334155; }

  .btn {
    padding: 12px 22px;
    border: none;
    border-radius: 10px;
    font-size: 0.9rem;
    font-family: 'Inter', sans-serif;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
    white-space: nowrap;
  }
  .btn-primary {
    background: #6366f1;
    color: white;
  }
  .btn-primary:hover { background: #4f46e5; transform: translateY(-1px); }
  .btn-primary:active { transform: translateY(0); }

  /* User list */
  .user-list { display: flex; flex-direction: column; gap: 10px; }

  .user-item {
    display: flex;
    align-items: center;
    gap: 14px;
    background: #0f0f13;
    border: 1px solid #2a2a38;
    border-radius: 12px;
    padding: 14px 16px;
    animation: slideIn 0.3s ease;
    transition: border-color 0.2s;
  }
  .user-item:hover { border-color: #3a3a50; }

  @keyframes slideIn {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
  }

  .avatar {
    width: 38px; height: 38px;
    border-radius: 50%;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    display: flex; align-items: center; justify-content: center;
    font-weight: 600; font-size: 0.95rem; color: white;
    flex-shrink: 0;
  }

  .user-info { flex: 1; }
  .user-name { font-weight: 500; color: #f1f5f9; font-size: 0.95rem; }
  .user-id   { font-size: 0.75rem; color: #334155; margin-top: 2px; }

  .delete-btn {
    background: none; border: none; cursor: pointer;
    color: #334155; font-size: 1rem; padding: 4px 8px;
    border-radius: 6px; transition: all 0.2s;
  }
  .delete-btn:hover { background: rgba(239,68,68,0.1); color: #ef4444; }

  /* Toast */
  .toast {
    position: fixed; bottom: 24px; right: 24px;
    background: #1e1e2e; border: 1px solid #2a2a38;
    border-radius: 12px; padding: 14px 20px;
    font-size: 0.9rem; color: #e2e8f0;
    display: flex; align-items: center; gap: 10px;
    transform: translateY(80px); opacity: 0;
    transition: all 0.35s cubic-bezier(0.34,1.56,0.64,1);
    z-index: 999;
  }
  .toast.show { transform: translateY(0); opacity: 1; }
  .toast.success { border-color: rgba(34,197,94,0.3); }
  .toast.error   { border-color: rgba(239,68,68,0.3); }

  /* Empty state */
  .empty {
    text-align: center; padding: 40px 20px;
    color: #334155; font-size: 0.9rem;
  }
  .empty-icon { font-size: 2.5rem; margin-bottom: 12px; }

  @media(max-width:480px) {
    .input-row { flex-direction: column; }
    .stats { flex-direction: column; }
  }
</style>
</head>
<body>
<div class="container">

  <div class="header">
    <div class="badge">⚡ Flask + SQLite</div>
    <h1>User Manager</h1>
    <p>Add, view and manage users in your database</p>
  </div>

  <div class="stats">
    <div class="stat-card">
      <span class="stat-num" id="totalCount">0</span>
      <div class="stat-label">Total Users</div>
    </div>
    <div class="stat-card">
      <span class="stat-num" id="lastAdded">—</span>
      <div class="stat-label">Last Added</div>
    </div>
  </div>

  <div class="card">
    <div class="card-title">Add User</div>
    <div class="input-row">
      <input type="text" id="nameInput" placeholder="Enter a name..." onkeydown="if(event.key==='Enter') addUser()">
      <button class="btn btn-primary" onclick="addUser()">+ Add</button>
    </div>
  </div>

  <div class="card">
    <div class="card-title">Users</div>
    <div class="user-list" id="userList">
      <div class="empty"><div class="empty-icon">👤</div>No users yet. Add one above!</div>
    </div>
  </div>

</div>

<!-- Toast -->
<div class="toast" id="toast"></div>

<script>
async function loadUsers() {
  const res = await fetch('/users');
  const users = await res.json();
  const list = document.getElementById('userList');
  document.getElementById('totalCount').textContent = users.length;

  if(users.length === 0) {
    list.innerHTML = '<div class="empty"><div class="empty-icon">👤</div>No users yet. Add one above!</div>';
    document.getElementById('lastAdded').textContent = '—';
    return;
  }

  document.getElementById('lastAdded').textContent = users[users.length-1].name.slice(0,8) + (users[users.length-1].name.length>8?'…':'');

  list.innerHTML = users.map(u => `
    <div class="user-item" id="user-${u.id}">
      <div class="avatar">${u.name.charAt(0).toUpperCase()}</div>
      <div class="user-info">
        <div class="user-name">${u.name}</div>
        <div class="user-id">ID #${u.id}</div>
      </div>
      <button class="delete-btn" onclick="deleteUser(${u.id})" title="Remove">✕</button>
    </div>
  `).join('');
}

async function addUser() {
  const input = document.getElementById('nameInput');
  const name = input.value.trim();
  if(!name) { showToast('⚠️ Please enter a name', 'error'); return; }

  const res = await fetch('/users', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({name})
  });

  if(res.ok) {
    input.value = '';
    showToast('✅ ' + name + ' added!', 'success');
    loadUsers();
  } else {
    showToast('❌ Something went wrong', 'error');
  }
}

async function deleteUser(id) {
  const res = await fetch('/users/' + id, { method: 'DELETE' });
  if(res.ok) { showToast('🗑️ User removed', 'success'); loadUsers(); }
}

function showToast(msg, type='success') {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.className = 'toast ' + type + ' show';
  setTimeout(() => t.classList.remove('show'), 2800);
}

loadUsers();
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/users", methods=["POST"])
def add_user():
    data = request.get_json()
    user = User(name=data["name"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User added", "id": user.id}), 201

@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([{"id": u.id, "name": u.name} for u in users])

@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
