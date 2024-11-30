import { createBrowserRouter } from "react-router-dom"
import Landing from "../pages/Landing"
import Register from "../pages/Register"
import Productpage from "../components/General/Productpage"

const routes = createBrowserRouter([
    {
        path:"/",
        element:<Landing/>
    },
    {
        path:"/register",
        element:<Register/>
    },
    {
        path:"/product",
        element:<Productpage/>
    },

])

export default routes