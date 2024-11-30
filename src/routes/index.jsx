import { createBrowserRouter } from "react-router-dom"
import Landing from "../pages/Landing"
import Register from "../pages/Register"

const routes = createBrowserRouter([
    {
        path:"/",
        element:<Landing/>
    },
    {
        path:"/register",
        element:<Register/>
    },

])

export default routes