import { createRouter, createWebHistory } from 'vue-router'

import HomePage from './pages/HomePage.vue'
import TasksLayout from './pages/TasksLayout.vue'
import TasksListPage from './pages/TasksListPage.vue'
import TaskNewPage from './pages/TaskNewPage.vue'
import TaskEditPage from './pages/TaskEditPage.vue'
import MonthPage from './pages/MonthPage.vue'
import NotFoundPage from './pages/NotFoundPage.vue'

const routes = [
  { path: '/', name: 'home', component: HomePage },

  // Вложенные маршруты: /tasks — layout, внутри разные страницы
  {
    path: '/tasks',
    name: 'tasks-layout',
    component: TasksLayout,
    children: [
      { path: '', name: 'tasks', component: TasksListPage },
      { path: 'new', name: 'task-new', component: TaskNewPage },
      { path: ':id/edit', name: 'task-edit', component: TaskEditPage },
    ],
  },

  { path: '/month', name: 'month', component: MonthPage },

  { path: '/:pathMatch(.*)*', name: 'not-found', component: NotFoundPage },
]

export const router = createRouter({
  history: createWebHistory(),
  routes,
})
