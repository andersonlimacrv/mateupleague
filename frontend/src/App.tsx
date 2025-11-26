import { Header } from "@/components/layout/header";
import InteractiveDotBackground from "@/components/layout/dot-background";

function App() {
  return (
    <div className="w-full">
      <Header />
      <main className="mx-auto min-h-screen w-full">
        <InteractiveDotBackground />
      </main>
    </div>
  );
}

export default App;
