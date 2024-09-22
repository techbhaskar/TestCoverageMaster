import { Component } from '@angular/core';
import { TaskService } from '../task.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-task-create',
  templateUrl: './task-create.component.html',
  styleUrls: ['./task-create.component.css']
})
export class TaskCreateComponent {
  constructor(private taskService: TaskService, private router: Router) { }

  createTask(title: string, description: string): void {
    if (!title || !description) return;

    this.taskService.addTask({ title, description, status: 'todo' } as any)
      .subscribe(() => {
        this.router.navigate(['/']);
      });
  }
}
