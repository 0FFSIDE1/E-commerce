import { createBrowserRouter } from "react-router-dom"
import Landing from "../pages/Landing"
import Register from "../pages/Register"
import Productpage from "../components/General/Productpage"
import VendorPage from "../pages/VendorPage"

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
    {
        path:"/vendor",
        element:<VendorPage/>
    },

])

export default routes