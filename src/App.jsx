import { RouterProvider } from "react-router-dom";
import routes from "./routes";
import AuthProvider from "./routes/AuthContext";

function App() {
  return (
    <AuthProvider>  {/* app with AuthProvider */}
      <RouterProvider router={routes}/>
    </AuthProvider>
  );
}

export default App;
