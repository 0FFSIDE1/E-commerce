import { RouterProvider } from "react-router-dom";
import routes from "./routes";
import AuthProvider from "./routes/AuthContext";

function App() {
  return (
    <AuthProvider>  {/* app with AuthProvider */}
      <RouterProvider router={routes} future={{ v7_startTransition: true }}/>
    </AuthProvider>
  );
}

export default App;
