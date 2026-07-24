// Ajusta esta URL si el prefijo de tus endpoints en FastAPI cambia
const API_URL = "http://localhost:8000/api/v1"; 

let repoModal;

// Cargar datos automáticamente al abrir la página
document.addEventListener("DOMContentLoaded", () => {
    const modalElement = document.getElementById('repoModal');
    if (modalElement) {
        repoModal = new bootstrap.Modal(modalElement);
    }
    fetchRepositories();
});

/**
 * Función auxiliar para asegurar que las URLs tengan el protocolo https://
 */
function normalizeUrl(url) {
    if (!url) return '';
    const trimmed = String(url).trim();
    if (!trimmed) return '';
    if (!trimmed.startsWith('http://') && !trimmed.startsWith('https://')) {
        return `https://${trimmed}`;
    }
    return trimmed;
}

/**
 * 1. OBTENER Y MOSTRAR REPOSITORIOS (READ)
 */
async function fetchRepositories() {
    const tableBody = document.getElementById('repoTableBody');
    if (!tableBody) return;

    tableBody.innerHTML = `
        <tr>
            <td colspan="6" class="text-center py-5 text-muted">
                <div class="spinner-border spinner-border-sm text-primary me-2" role="status"></div>
                Cargando repositorios...
            </td>
        </tr>`;

    try {
        const response = await fetch(`${API_URL}/repositories`);
        
        if (!response.ok) {
            throw new Error(`HTTP Error ${response.status}`);
        }

        const repos = await response.json();
        tableBody.innerHTML = '';

        if (!Array.isArray(repos) || repos.length === 0) {
            tableBody.innerHTML = `
                <tr>
                    <td colspan="6" class="text-center py-4 text-muted">
                        <i class="bi bi-inbox fs-3 d-block mb-2"></i>
                        No hay repositorios guardados en la base de datos.
                    </td>
                </tr>`;
            return;
        }

        repos.forEach(repo => {
            // Se usa encodeURIComponent para pasar el objeto de forma segura al modal
            const repoJson = encodeURIComponent(JSON.stringify(repo));
            
            // Garantizar que la URL sea absoluta para no causar un 404 local
            const githubUrl = normalizeUrl(repo.html_url);

            tableBody.innerHTML += `
                <tr>
                    <td class="ps-4 fw-bold text-secondary">#${repo.id}</td>
                    <td class="fw-bold text-dark">${escapeHtml(repo.name)}</td>
                    <td><span class="text-muted">@${escapeHtml(repo.owner || 'N/A')}</span></td>
                    <td><span class="badge badge-language px-2 py-1">${escapeHtml(repo.language || 'N/A')}</span></td>
                    <td><span class="text-warning fw-bold"><i class="bi bi-star-fill me-1"></i>${repo.stars || 0}</span></td>
                    <td class="text-end pe-4">
                        <button class="btn btn-outline-warning btn-action me-1" onclick="handleEditClick('${repoJson}')" title="Editar">
                            <i class="bi bi-pencil-fill"></i>
                        </button>
                        <button class="btn btn-outline-danger btn-action me-1" onclick="deleteRepository(${repo.id})" title="Eliminar">
                            <i class="bi bi-trash-fill"></i>
                        </button>
                        ${githubUrl ? `
                        <a href="${escapeHtml(githubUrl)}" target="_blank" rel="noopener noreferrer" class="btn btn-outline-dark btn-action" title="Abrir en GitHub">
                            <i class="bi bi-box-arrow-up-right"></i>
                        </a>` : ''}
                    </td>
                </tr>
            `;
        });
    } catch (error) {
        console.error("Error al obtener repositorios:", error);
        tableBody.innerHTML = `
            <tr>
                <td colspan="6" class="text-center py-4 text-danger">
                    <i class="bi bi-exclamation-triangle-fill fs-3 d-block mb-2"></i>
                    Error de conexión con FastAPI (${escapeHtml(error.message)}). Revisa si el servidor está corriendo y CORS habilitado.
                </td>
            </tr>`;
    }
}

/**
 * 2. SINCRONIZAR DESDE GITHUB
 */
async function syncGithub() {
    const usernameInput = document.getElementById('usernameInput');
    const statusDiv = document.getElementById('syncStatus');

    if (!usernameInput) {
        console.error("No se encontró el input 'usernameInput'");
        return;
    }

    const username = usernameInput.value.trim();

    if (!username) {
        if (statusDiv) statusDiv.innerHTML = `<span class="text-danger">Por favor ingresa un usuario de GitHub.</span>`;
        return;
    }

    if (statusDiv) {
        statusDiv.innerHTML = `<span class="text-primary"><div class="spinner-border spinner-border-sm me-1"></div> Sincronizando repositorios de ${escapeHtml(username)}...</span>`;
    }

    try {
        const response = await fetch(`${API_URL}/sync/${encodeURIComponent(username)}`, { 
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });

        const result = await response.json().catch(() => ({}));

        if (response.ok) {
            if (statusDiv) {
                statusDiv.innerHTML = `<span class="text-success">✅ ${escapeHtml(result.message || 'Sincronización realizada correctamente.')}</span>`;
            }
            fetchRepositories(); // Refresca la tabla automáticamente
        } else {
            console.error("Error del servidor en sync:", result);
            if (statusDiv) {
                const detail = typeof result.detail === 'string' ? result.detail : (result.message || 'No se pudo sincronizar.');
                statusDiv.innerHTML = `<span class="text-danger">❌ Error (${response.status}): ${escapeHtml(detail)}</span>`;
            }
        }
    } catch (error) {
        console.error("Error de red al sincronizar:", error);
        if (statusDiv) {
            statusDiv.innerHTML = `<span class="text-danger">❌ Error de conexión: ${escapeHtml(error.message)}</span>`;
        }
    }
}

/**
 * 3. GUARDAR REPOSITORIO (CREATE / UPDATE)
 */
async function saveRepository() {
    const id = document.getElementById('repoId').value;
    const name = document.getElementById('repoName').value.trim();
    const owner = document.getElementById('repoOwner').value.trim();
    const language = document.getElementById('repoLanguage').value.trim();
    const stars = parseInt(document.getElementById('repoStars').value) || 0;
    const rawUrl = document.getElementById('repoUrl').value.trim();

    if (!name || !owner) {
        alert("El Nombre del Repositorio y el Propietario son obligatorios.");
        return;
    }

    // Asegurar formato de URL adecuado antes de enviarla a FastAPI
    const html_url = normalizeUrl(rawUrl);

    const isEdit = id !== "";

    // Construcción del objeto payload
    const payload = { 
        name, 
        owner, 
        language, 
        stars, 
        html_url 
    };

    // Si es CREACIÓN, enviamos github_id y full_name requeridos por Pydantic
    if (!isEdit) {
        payload.github_id = Math.floor(100000 + Math.random() * 900000); // ID numérico aleatorio
        payload.full_name = `${owner}/${name}`;
    }

    const url = isEdit ? `${API_URL}/repositories/${id}` : `${API_URL}/repositories`;
    const method = isEdit ? 'PUT' : 'POST';

    try {
        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            if (repoModal) repoModal.hide();
            fetchRepositories();
        } else {
            const errData = await response.json().catch(() => ({}));
            console.error("Error en saveRepository:", errData);
            const msg = typeof errData.detail === 'string' 
                ? errData.detail 
                : JSON.stringify(errData.detail || errData);
            alert(`Error (${response.status}): ${msg}`);
        }
    } catch (error) {
        console.error("Error de solicitud:", error);
        alert(`Error de red al intentar guardar: ${error.message}`);
    }
}

/**
 * 4. ELIMINAR REPOSITORIO (DELETE)
 */
async function deleteRepository(id) {
    if (!confirm(`¿Estás seguro de que deseas eliminar el repositorio #${id}?`)) return;

    try {
        const response = await fetch(`${API_URL}/repositories/${id}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            fetchRepositories();
        } else {
            const errData = await response.json().catch(() => ({}));
            alert(`No se pudo eliminar el registro (#${id}): ${errData.detail || 'Error en la petición'}`);
        }
    } catch (error) {
        console.error("Error de red al eliminar:", error);
        alert(`Error de conexión al eliminar: ${error.message}`);
    }
}

// Helper para limpiar/preparar el modal de creación
function openCreateModal() {
    const form = document.getElementById('repoForm');
    if (form) form.reset();
    document.getElementById('repoId').value = '';
    document.getElementById('repoModalTitle').innerText = 'Crear Nuevo Repositorio';
    if (repoModal) repoModal.show();
}

// Auxiliar para desempaquetar el objeto codificado antes de abrir el modal
function handleEditClick(encodedRepo) {
    try {
        const repo = JSON.parse(decodeURIComponent(encodedRepo));
        openEditModal(repo);
    } catch (e) {
        console.error("Error al decodificar datos del repositorio:", e);
    }
}

// Helper para cargar los datos en el modal de edición
function openEditModal(repo) {
    document.getElementById('repoId').value = repo.id || '';
    document.getElementById('repoName').value = repo.name || '';
    document.getElementById('repoOwner').value = repo.owner || '';
    document.getElementById('repoLanguage').value = repo.language || '';
    document.getElementById('repoStars').value = repo.stars || 0;
    document.getElementById('repoUrl').value = repo.html_url || '';
    document.getElementById('repoModalTitle').innerText = `Editar Repositorio #${repo.id}`;
    if (repoModal) repoModal.show();
}

// Función auxiliar para prevenir inyección de caracteres en el HTML
function escapeHtml(text) {
    if (!text) return '';
    return String(text)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}