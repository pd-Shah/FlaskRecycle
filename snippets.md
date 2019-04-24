```html
<span class="icon">
  <i class="io ion-ios-circle-outline" onclick="updateTaskStatus({{ task.id }}, 4)"></i>
</span>
```

```javascript
let csrf_token = $('meta[name=csrf-token]');
let request = superagent;
function updateTaskStatus (t, s) {
    let element = "#task_" + t
    console.log(t + ' ' + s);
    request.post('/account/tasks/update/status')
      .type('form')
      .send({ task_id: t })
      .send({ task_new_status: s })
      .send({ csrf_token: csrf_token.value[0].content })
      .then(res => {
          $(element).addClass("is-done");
        console.log()
      })
      .catch(err => {
        console.log(err)
      });
}
```