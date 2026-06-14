// js/utils/routes.js

/** 
 * Official frontend route mapping matching the backend Role Enum values 1:1.
 * @type {Object.<string, string>}
 */
export const ROLE_ROUTES = {
    'client': '/',
    'receptionist': '/admin/reception', // ◄ Cambiado a 'reception'
    'supervisor': '/admin/supervisor',   // ◄ Este ya estaba perfecto
    'manager': '/admin/manager'         // ◄ Cambiado a 'manager'
};

/**
 * Handles the user redirection based on their assigned role.
 * @param {string} role - The role string returned by the Auth API.
 */
export const redirectByUserRole = (role) => {
    // Exact match with your Enum strings ('client', 'receptionist', 'supervisor', 'manager')
    const targetRoute = ROLE_ROUTES[role];

    if (targetRoute) {
        // Special flow for clients to preserve cart or booking redirects
        if (role === 'client') {
            const redirectUrl = localStorage.getItem('redirect_after_login') || targetRoute;
            localStorage.removeItem('redirect_after_login');
            window.location.href = redirectUrl;
            return;
        }
        
        // Direct redirection for administrative roles
        window.location.href = targetRoute;
    } else {
        console.error(`The role "${role}" has no matching route configured.`);
        window.location.href = '/auth/login';
    }
};