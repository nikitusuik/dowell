const API_BASE = ''

async function request(path, options = {}) {
  const res = await fetch(API_BASE + path, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })

  // 204 No Content
  if (res.status === 204) return null

  const data = await res.json().catch(() => null)

  if (!res.ok) {
    const message = data?.detail || `HTTP ${res.status}`
    throw new Error(message)
  }

  return data
}

export function fetchTasks() {
  return request('/api/tasks')
}

export function createTask(payload) {
  return request('/api/tasks', { method: 'POST', body: JSON.stringify(payload) })
}

export function deleteTask(id) {
  return request(`/api/tasks/${id}`, { method: 'DELETE' })
}

export function submitToday(items) {
  return request('/api/logs/today/submit', {
    method: 'POST',
    body: JSON.stringify({ items }),
  })
}

export function fetchMonthLogs() {
  return request('/api/logs/month')
}
export function fetchTask(id) {
  return request(`/api/tasks/${id}`)
}

export function updateTask(id, payload) {
  return request(`/api/tasks/${id}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  })
}
export function setTaskActive(id, active) {
  return request(`/api/tasks/${id}`, {
    method: 'PUT',
    body: JSON.stringify({ active }),
  })
}
