(this["webpackJsonperp-frontend"]=this["webpackJsonperp-frontend"]||[]).push([[110],{879:function(e,a,t){"use strict";t.r(a);var s=t(15),r=t.n(s),c=t(28),n=t(1),o=t(47),l=t(0),m=t.n(l),d=(t(9),t(500),t(2)),i=(t(84),t(29),t(13),t(31),t(258)),u=t(576),p=t(475),b=t(25),h=t(33),w=e=>{var a=m.a.useState(""),t=Object(o.a)(a,2),s=t[0],l=t[1],d=m.a.useState({}),w=Object(o.a)(d,2),f=w[0],E=w[1],y=e.location.search,j=(new URLSearchParams(y)||"").get("email")||"";Object(u.a)(j)||(j="");var N=function(){var a=Object(c.a)(r.a.mark((function a(){var t,c,o;return r.a.wrap((function(a){for(;;)switch(a.prev=a.next){case 0:if(t=Object(u.b)(s),c=t.isValid,o=t.errors,c){a.next=4;break}return E(o),a.abrupt("return");case 4:Object(p.e)({code:s}).then(a=>{console.log(a),a.json.status?(e.getCode(s),e.showResetPassword()):E(Object(n.a)(Object(n.a)({},o),{},{code:a.json.error}))}).catch(e=>console.log(e));case 5:case"end":return a.stop()}}),a)})));return function(){return a.apply(this,arguments)}}();return m.a.createElement("div",{className:"card-body text-center"},m.a.createElement("div",{className:"mb-4"},m.a.createElement("i",{className:"feather icon-unlock auth-icon"})),m.a.createElement("h3",{className:"mb-4"},"Reset Password"),m.a.createElement("p",{className:"mb-3 text-muted"},"Check your mail and enter the code you received."),m.a.createElement("div",{className:"input-group mb-3",style:{}},m.a.createElement("input",{name:"code",style:{display:"block",width:"100%"},type:"number",className:"form-control",placeholder:"Code",value:h.data.code,onChange:e=>{E(Object(n.a)(Object(n.a)({},f),{},{[e.target.name]:""})),l(e.target.value)},onKeyDown:e=>{"Enter"===e.key&&N()}}),m.a.createElement(i.a,null,f.code)),m.a.createElement("button",{className:"btn btn-primary shadow-2 mb-4",onClick:N},"Continue"),j?m.a.createElement("p",{className:"mb-0 text-muted"},"Didn't Receive Code?",m.a.createElement("span",{className:"btn-link",style:{cursor:"pointer"},onClick:()=>{j&&Object(p.d)({email:j}).then(a=>{console.log(a),a.json.status?b.a.fire({icon:"error",title:a.json.error,background:"#ffe5de"}):(b.a.fire({icon:"success",title:"Code send to the email successfully!",background:"#dffff0"}),e.history.push("/reset-password"))}).catch(e=>console.log(e))}},"  ","Resend")):null)};a.default=e=>{var a=m.a.useState(!1),t=Object(o.a)(a,2),s=t[0],l=t[1],h=m.a.useState({}),f=Object(o.a)(h,2),E=f[0],y=f[1],j=m.a.useState({password:"",password2:"",code:""}),N=Object(o.a)(j,2),g=N[0],v=N[1],O=()=>l(!0),k=e=>{y(Object(n.a)(Object(n.a)({},E),{},{[e.target.name]:""})),v(Object(n.a)(Object(n.a)({},g),{},{[e.target.name]:e.target.value}))},C=e=>{"Enter"===e.key&&x()},x=function(){var a=Object(c.a)(r.a.mark((function a(){var t,s,c;return r.a.wrap((function(a){for(;;)switch(a.prev=a.next){case 0:if(t=Object(u.c)(g),s=t.isValid,c=t.errors,s){a.next=4;break}return y(c),a.abrupt("return");case 4:console.log("Data is ",g),Object(p.c)({code:g.code,password:g.password}).then(a=>{console.log(a),a.json.status?(b.a.fire({icon:"success",title:"Password change successful!",background:"#dffff0"}),e.history.push("/signin")):b.a.fire({icon:"error",title:a.json.error,background:"#ffe5de"})}).catch(e=>console.log(e));case 6:case"end":return a.stop()}}),a)})));return function(){return a.apply(this,arguments)}}();return O?m.a.createElement(d.a,null,m.a.createElement("div",{className:"auth-wrapper"},m.a.createElement("div",{className:"auth-content"},m.a.createElement("div",{className:"auth-bg"},m.a.createElement("span",{className:"r"}),m.a.createElement("span",{className:"r s"}),m.a.createElement("span",{className:"r s"}),m.a.createElement("span",{className:"r"})),m.a.createElement("div",{className:"card"},s?m.a.createElement("div",{className:"card-body text-center"},m.a.createElement("div",{className:"mb-4"},m.a.createElement("i",{className:"feather icon-unlock auth-icon"})),m.a.createElement("h3",{className:"mb-4"},"Reset Password"),m.a.createElement("p",{className:"mb-3 text-muted"},"Get code to reset your password."),m.a.createElement("div",{className:"input-group mb-3",style:{}},m.a.createElement("input",{name:"password",style:{display:"block",width:"100%"},type:"password",className:"form-control",placeholder:"New Password",value:g.password,onChange:k,onKeyDown:C}),m.a.createElement(i.a,null,E.password)),m.a.createElement("div",{className:"input-group mb-3",style:{}},m.a.createElement("input",{name:"password2",style:{display:"block",width:"100%"},type:"password",className:"form-control",placeholder:"Confirm Password",value:g.password2,onChange:k,onKeyDown:C}),m.a.createElement(i.a,null,E.password2)),m.a.createElement("button",{className:"btn btn-primary shadow-2 mb-4",onClick:x},"Reset Password")):m.a.createElement(w,{location:e.location,showResetPassword:O,getCode:e=>{v(Object(n.a)(Object(n.a)({},g),{},{code:e}))}}))))):m.a.createElement(w,null)}}}]);
//# sourceMappingURL=110.a397c30f.chunk.js.map