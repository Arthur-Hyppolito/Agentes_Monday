import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

class GitSyncHandler(FileSystemEventHandler):
    def __init__(self, path):
        self.path = path
        self.last_sync = time.time()
        
    def on_modified(self, event):
        # Ignora alterações no .git e .env
        if '.git' in event.src_path or '.env' in event.src_path:
            return
            
        # Espera 2 segundos para evitar múltiplas sincronizações
        current_time = time.time()
        if current_time - self.last_sync < 2:
            return
            
        print("\nDetected changes. Starting sync...")
        try:
            # Adiciona as alterações
            subprocess.run(['git', 'add', '.'], cwd=self.path, capture_output=True)
            
            # Faz o commit com timestamp
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            subprocess.run(['git', 'commit', '-m', f'Automatic sync at {timestamp}'], cwd=self.path, capture_output=True)
            
            # Faz o push
            subprocess.run(['git', 'push'], cwd=self.path, capture_output=True)
            print("Sync completed successfully!")
            self.last_sync = current_time
            
        except Exception as e:
            print(f"Error during sync: {str(e)}")

def main():
    # Caminho do projeto
    project_path = os.path.dirname(os.path.abspath(__file__))
    
    # Inicializa o handler
    event_handler = GitSyncHandler(project_path)
    
    # Inicializa o observer
    observer = Observer()
    observer.schedule(event_handler, project_path, recursive=True)
    
    print("Starting automatic Git sync...")
    print("Monitoring directory:", project_path)
    print("Press Ctrl+C to stop.")
    
    # Inicia o observer
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
