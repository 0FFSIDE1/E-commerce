import { createBrowserRouter } from "react-router-dom"
import Landing from "../pages/Landing"
import Register from "../pages/Register"
import Productpage from "../pages/Productpage"
import VendorPage from "../pages/VendorPage"
import ProtectiveRoute from "./ProtectiveRoute"

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
        // This is meant to be a protective route
    },
    {
        path:"/vendor",
        element:<VendorPage/>
    },

])

export default routes