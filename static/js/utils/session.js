import { AuthServices } from "../services/AuthServices.js";
import { ROLE_ROUTES, redirectByUserRole } from "./routes.js";

export const authRequire = async () => {
    const jsonResponse = await AuthServices.checkAuth();

    if (!jsonResponse) {
        if (window.location.pathname !== '/auth/login') {
            window.location.href = '/auth/login';
        }
        return false;
    }

    const role = jsonResponse.role; 
    const currentPath = window.location.pathname;
    const expectedRoute = ROLE_ROUTES[role];

    if (currentPath === '/' || currentPath === '/auth/login') {
        redirectByUserRole(role);
        return true;
    }

    if (currentPath.startsWith('/panel') && currentPath !== expectedRoute) {
        console.warn(`Access denied. Redirecting to: ${role}`);
        redirectByUserRole(role); 
        return false;
    }

    return true;
};