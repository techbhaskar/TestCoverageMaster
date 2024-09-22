import { TestBed } from '@angular/core/testing';
import { TaskService } from './task.service';
import { Task } from './task';

describe('TaskService', () => {
  let service: TaskService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(TaskService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should return tasks', (done: DoneFn) => {
    service.getTasks().subscribe(tasks => {
      expect(tasks.length).toBeGreaterThan(0);
      done();
    });
  });

  it('should add a task', (done: DoneFn) => {
    const newTask: Task = { title: 'New Task', description: 'New Description', status: 'todo' } as any;
    service.addTask(newTask).subscribe(task => {
      expect(task.id).toBeDefined();
      expect(task.title).toBe('New Task');
      done();
    });
  });

  it('should update a task', (done: DoneFn) => {
    service.getTasks().subscribe(tasks => {
      const taskToUpdate = tasks[0];
      taskToUpdate.title = 'Updated Task';
      service.updateTask(taskToUpdate).subscribe(updatedTask => {
        expect(updatedTask.title).toBe('Updated Task');
        done();
      });
    });
  });

  it('should delete a task', (done: DoneFn) => {
    service.getTasks().subscribe(tasks => {
      const initialCount = tasks.length;
      const taskToDelete = tasks[0];
      service.deleteTask(taskToDelete.id).subscribe(() => {
        service.getTasks().subscribe(updatedTasks => {
          expect(updatedTasks.length).toBe(initialCount - 1);
          done();
        });
      });
    });
  });
});
