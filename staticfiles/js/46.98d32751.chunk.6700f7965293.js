(this["webpackJsonperp-frontend"]=this["webpackJsonperp-frontend"]||[]).push([[46],{194:function(e,t,n){"use strict";n.r(t);var a=n(20),r=n.n(a),c=n(1),o=n(2),s=n(33),i=n(55),u=n(0),l=n.n(u),p=n(296),h=n(264),f=n(313),d=n(306),m=n(111),b=n(286),v=n.n(b),y=n(3),O=n(276),j=n(451),g=n(262),x=n(30),w=n(431),E=n(263),k=n(311),C=n(271),S=n(36);t.default=function(e){var t=l.a.useState(!0),n=Object(i.a)(t,2),a=n[0],u=n[1],b=l.a.useState([]),T=Object(i.a)(b,2),N=T[0],P=T[1],M=l.a.useState(!1),L=Object(i.a)(M,2),_=L[0],D=L[1],R=l.a.useState({id:"",fname:"",lname:"",mname:"",category:"",email:"",website:"",tax:"",phone1:"",phone2:"",address:"",country:"",countryName:"",isActive:!1}),A=Object(i.a)(R,2),G=A[0],I=A[1],B=l.a.useState([]),z=Object(i.a)(B,2),H=z[0],W=z[1],F=l.a.useState({}),U=Object(i.a)(F,2),X=U[0],Z=U[1];l.a.useEffect((function(){var t=new AbortController;return Object(s.a)(r.a.mark((function n(){return r.a.wrap((function(n){for(;;)switch(n.prev=n.next){case 0:0,Object(w.c)({action:"get",filter:"none",start:0,end:999999},t.signal).then((function(e){console.log(e),e.json.status?(P(Object(o.a)(e.json.customerCategories)),u(!1)):x.a.fire({icon:"error",title:e.json.error,background:"#ffe5de"})})).catch((function(e){console.log(e)})),Object(C.g)({action:"get"},t.signal).then((function(e){console.log(e),e.json.status&&(W(Object(o.a)(e.json.countries.map((function(e){return{label:e.name,value:e.id}})))))})).catch((function(e){console.log(e)})),Object(k.c)({action:"get",customer_id:e.match.params.id,filter:"none"},t.signal).then(function(){var e=Object(s.a)(r.a.mark((function e(t){var n;return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(console.log(t.json),!t.json.status){e.next=8;break}return n=t.json.customers[0],e.next=5,I(Object(c.a)(Object(c.a)({},G),{},{id:n.id,fname:n.first_name,lname:n.last_name,mname:n.middle_name,category:n.category,email:n.email,website:n.website,tax:n.tax_number,phone1:n.phone1,phone2:n.phone2,address:n.address,country:n.country,countryName:n.country_detail.name,isActive:n.is_active}));case 5:u(!1),e.next=9;break;case 8:x.a.fire({icon:"error",title:t.json.error,background:"#ffe5de"});case 9:case"end":return e.stop()}}),e)})));return function(t){return e.apply(this,arguments)}}()).catch((function(e){console.log(e)}));case 4:case"end":return n.stop()}}),n)})))(),function(){return t.abort()}}),[]);var $=function(e){console.log("chaing",e.target.value),Z(Object(c.a)(Object(c.a)({},X),{},{[e.target.name]:""})),I(Object(c.a)(Object(c.a)({},G),{},{[e.target.name]:e.target.value}))};return console.log(G),a?l.a.createElement(E.a,null):l.a.createElement(y.a,null,l.a.createElement(p.a,null,l.a.createElement(h.a,null,l.a.createElement(f.a,null,l.a.createElement(f.a.Body,null,l.a.createElement("h5",null,"Update Customer"),l.a.createElement("hr",null),l.a.createElement(p.a,null,l.a.createElement(h.a,{md:4},l.a.createElement(d.a.Group,null,l.a.createElement(d.a.Label,null,"First Name*"),l.a.createElement(d.a.Control,{name:"fname",value:G.fname,onChange:$,type:"text",placeholder:"First Name"}),l.a.createElement(g.a,null,X.fname))),l.a.createElement(h.a,{md:4},l.a.createElement(d.a.Group,null,l.a.createElement(d.a.Label,null,"Middle Name"),l.a.createElement(d.a.Control,{name:"mname",value:G.mname||"",onChange:$,type:"text",placeholder:"Middle Name"}),l.a.createElement(g.a,null,X.mname))),l.a.createElement(h.a,{md:4},l.a.createElement(d.a.Group,null,l.a.createElement(d.a.Label,null,"Last Name*"),l.a.createElement(d.a.Control,{name:"lname",value:G.lname,onChange:$,type:"text",placeholder:"Last Name"}),l.a.createElement(g.a,null,X.lname))),l.a.createElement(h.a,{md:6},l.a.createElement(d.a.Group,null,l.a.createElement(d.a.Label,null,"Customer Category*"),l.a.createElement(d.a.Control,{name:"category",value:G.category,onChange:$,as:"select"},l.a.createElement("option",{value:"",disabled:!0},"Select Customer Category"),N.map((function(e,t){return l.a.createElement("option",{key:t,value:e.id},e.name)}))),l.a.createElement(g.a,null,X.category))),l.a.createElement(h.a,{md:6},l.a.createElement(d.a.Group,null,l.a.createElement(d.a.Label,null,"Email*"),l.a.createElement(d.a.Control,{name:"email",value:G.email,onChange:$,type:"email",placeholder:"Email"}),l.a.createElement(g.a,null,X.email))),l.a.createElement(h.a,{md:6},l.a.createElement(d.a.Group,null,l.a.createElement(d.a.Label,null,"Address"),l.a.createElement(d.a.Control,{name:"address",value:G.address,onChange:$,type:"text",placeholder:"Address"}),l.a.createElement(g.a,null,X.address))),l.a.createElement(h.a,{md:6},l.a.createElement(d.a.Group,null,l.a.createElement(d.a.Label,null,"Phone No 1*"),l.a.createElement(d.a.Control,{name:"phone1",value:G.phone1,onChange:$,type:"tel",placeholder:"Phone No 1"}),l.a.createElement(g.a,null,X.phone1))),l.a.createElement(h.a,{md:6},l.a.createElement(d.a.Group,null,l.a.createElement(d.a.Label,null,"Phone No 2"),l.a.createElement(d.a.Control,{name:"phone2",value:G.phone2,onChange:$,type:"tel",placeholder:"Phone No 2"}),l.a.createElement(g.a,null,X.phone2))),l.a.createElement(h.a,{md:6},l.a.createElement(d.a.Group,null,l.a.createElement(d.a.Label,null,"Tax Number*"),l.a.createElement(d.a.Control,{name:"tax",value:G.tax,onChange:$,type:"number",placeholder:"Tax Number"}),l.a.createElement(g.a,null,X.tax))),l.a.createElement(h.a,{md:6},l.a.createElement(d.a.Group,null,l.a.createElement(d.a.Label,null,"Website"),l.a.createElement(d.a.Control,{name:"website",value:G.website,onChange:$,type:"text",placeholder:"Website"}),l.a.createElement(g.a,null,X.website))),l.a.createElement(h.a,{md:6},l.a.createElement(d.a.Group,null,l.a.createElement(d.a.Label,null,"Country"),l.a.createElement(O.a,{value:Object(S.a)(G.country)?null:{value:G.country,label:G.countryName},onChange:function(e){return t=e,Z(Object(c.a)(Object(c.a)({},X),{},{country:""})),void I(Object(c.a)(Object(c.a)({},G),{},{country:t.value,countryName:t.label}));var t},options:H,placeholder:"Select Country"}),l.a.createElement(g.a,null,X.country))),l.a.createElement(h.a,{md:6},l.a.createElement(d.a.Group,{className:"d-flex flex-column justify-content-end"},l.a.createElement(d.a.Label,{style:{marginBottom:"15px"}},"Is Active?"),l.a.createElement(v.a,{onChange:function(e){console.log(e),I(Object(c.a)(Object(c.a)({},G),{},{isActive:e}))},checked:G.isActive})))),l.a.createElement("div",{className:"d-flex justify-content-end"},l.a.createElement(m.a,{variant:"warning",onClick:function(){e.history.push("/customers")}},"Cancel"),l.a.createElement(m.a,{disabled:_,variant:"primary",onClick:function(){var t=Object(j.a)(G),n=t.isValid,a=t.errors;if(!n)return console.log(a),void Z(Object(c.a)({},a));console.log("no errros"),D(!0);var r={action:"update",id:G.id,first_name:G.fname,last_name:G.lname,middle_name:G.mname,category:parseInt(G.category),email:G.email,website:G.website,tax_number:parseFloat(G.tax),phone1:G.phone1,phone2:G.phone2,address:G.address,country:G.country,is_active:G.isActive};Object(k.e)(r).then((function(t){console.log(t),t.json.status?(D(!1),x.a.fire({icon:"success",title:"Customer updated successfully!",background:"#dffff0"}),e.history.push("/customers")):(D(!1),x.a.fire({icon:"error",title:t.json.error,background:"#ffe5de"}))})).catch((function(e){D(!1),console.log(e)}))}},_?l.a.createElement(l.a.Fragment,null,l.a.createElement("i",{className:"fa fa-spinner text-c-white f-15 fa-pulse m-l-1"}),"Updating"):"Update")))))))}},262:function(e,t,n){"use strict";var a=n(0),r=n.n(a),c=n(306),o=n(36);t.a=function(e){return Object(o.a)(e.children)?r.a.createElement("span",null):r.a.createElement(r.a.Fragment,null,r.a.createElement(c.a.Text,{style:{color:"red"}},e.children))}},263:function(e,t,n){"use strict";var a=n(0),r=n.n(a);t.a=function(){return r.a.createElement("div",{className:"loader-bg"},r.a.createElement("div",{className:"loader-track"},r.a.createElement("div",{className:"loader-fill"})))}},264:function(e,t,n){"use strict";var a=n(6),r=n(8),c=n(11),o=n.n(c),s=n(0),i=n.n(s),u=n(19),l=["xl","lg","md","sm","xs"],p=i.a.forwardRef((function(e,t){var n=e.bsPrefix,c=e.className,s=e.as,p=void 0===s?"div":s,h=Object(r.a)(e,["bsPrefix","className","as"]),f=Object(u.b)(n,"col"),d=[],m=[];return l.forEach((function(e){var t,n,a,r=h[e];if(delete h[e],null!=r&&"object"===typeof r){var c=r.span;t=void 0===c||c,n=r.offset,a=r.order}else t=r;var o="xs"!==e?"-"+e:"";null!=t&&d.push(!0===t?""+f+o:""+f+o+"-"+t),null!=a&&m.push("order"+o+"-"+a),null!=n&&m.push("offset"+o+"-"+n)})),d.length||d.push(f),i.a.createElement(p,Object(a.a)({},h,{ref:t,className:o.a.apply(void 0,[c].concat(d,m))}))}));p.displayName="Col",t.a=p},266:function(e,t,n){"use strict";var a=n(6),r=n(0),c=n.n(r),o=n(11),s=n.n(o);t.a=function(e){return c.a.forwardRef((function(t,n){return c.a.createElement("div",Object(a.a)({},t,{ref:n,className:s()(t.className,e)}))}))}},271:function(e,t,n){"use strict";n.d(t,"j",(function(){return y})),n.d(t,"b",(function(){return O})),n.d(t,"o",(function(){return g})),n.d(t,"e",(function(){return j})),n.d(t,"k",(function(){return v})),n.d(t,"i",(function(){return s})),n.d(t,"a",(function(){return u})),n.d(t,"d",(function(){return i})),n.d(t,"n",(function(){return p})),n.d(t,"h",(function(){return l})),n.d(t,"m",(function(){return h})),n.d(t,"c",(function(){return d})),n.d(t,"f",(function(){return f})),n.d(t,"p",(function(){return b})),n.d(t,"l",(function(){return m})),n.d(t,"g",(function(){return x}));var a=n(20),r=n.n(a),c=n(33),o=n(47),s=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/sales/discounts/get","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),i=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/sales/discounts/delete","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),u=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/sales/discount/add","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),l=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/sales/discount/get","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),p=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/sales/discount/update","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),h=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/sales/taxes/get","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),f=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/sales/taxes/delete","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),d=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/sales/tax/add","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),m=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/sales/tax/get","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),b=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/sales/tax/update","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),v=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/inventory/purchaseorders/status","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),y=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/inventory/placements/get","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),O=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/inventory/placements/assign","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),j=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/inventory/placements/assign","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),g=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/inventory/placements/assign","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),x=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/user/countries/get ","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}()},276:function(e,t,n){"use strict";n(308),n(299),n(327),n(309);var a=n(300),r=n(301),c=n(302),o=n(304),s=n(307),i=n(293),u=n(292),l=n(0),p=n.n(l),h=n(317),f=n(312),d=(n(40),n(7),n(303),n(268)),m=(n(289),n(315),n(316),n(331)),b=n(446),v=(l.Component,Object(m.a)(d.a));t.a=v},286:function(e,t,n){e.exports=n(288)},288:function(e,t,n){Object.defineProperty(t,"__esModule",{value:!0});var a=n(0);function r(){return(r=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var a in n)Object.prototype.hasOwnProperty.call(n,a)&&(e[a]=n[a])}return e}).apply(this,arguments)}var c=a.createElement("svg",{viewBox:"-2 -5 14 20",height:"100%",width:"100%",style:{position:"absolute",top:0}},a.createElement("path",{d:"M9.9 2.12L7.78 0 4.95 2.828 2.12 0 0 2.12l2.83 2.83L0 7.776 2.123 9.9 4.95 7.07 7.78 9.9 9.9 7.776 7.072 4.95 9.9 2.12",fill:"#fff",fillRule:"evenodd"})),o=a.createElement("svg",{height:"100%",width:"100%",viewBox:"-2 -5 17 21",style:{position:"absolute",top:0}},a.createElement("path",{d:"M11.264 0L5.26 6.004 2.103 2.847 0 4.95l5.26 5.26 8.108-8.107L11.264 0",fill:"#fff",fillRule:"evenodd"}));function s(e){if(7===e.length)return e;for(var t="#",n=1;n<4;n+=1)t+=e[n]+e[n];return t}function i(e,t,n,a,r){return function(e,t,n,a,r){var c=(e-n)/(t-n);if(0===c)return a;if(1===c)return r;for(var o="#",s=1;s<6;s+=2){var i=parseInt(a.substr(s,2),16),u=parseInt(r.substr(s,2),16),l=Math.round((1-c)*i+c*u).toString(16);1===l.length&&(l="0"+l),o+=l}return o}(e,t,n,s(a),s(r))}var u=function(e){function t(t){e.call(this,t);var n=t.height,a=t.width,r=t.checked;this.t=t.handleDiameter||n-2,this.i=Math.max(a-n,a-(n+this.t)/2),this.o=Math.max(0,(n-this.t)/2),this.state={s:r?this.i:this.o},this.n=0,this.e=0,this.h=this.h.bind(this),this.r=this.r.bind(this),this.a=this.a.bind(this),this.c=this.c.bind(this),this.l=this.l.bind(this),this.u=this.u.bind(this),this.f=this.f.bind(this),this.p=this.p.bind(this),this.b=this.b.bind(this),this.g=this.g.bind(this),this.v=this.v.bind(this),this.w=this.w.bind(this)}return e&&(t.__proto__=e),((t.prototype=Object.create(e&&e.prototype)).constructor=t).prototype.componentDidUpdate=function(e){e.checked!==this.props.checked&&this.setState({s:this.props.checked?this.i:this.o})},t.prototype.k=function(e){this.y.focus(),this.setState({C:e,M:!0,m:Date.now()})},t.prototype.x=function(e){var t=this.state,n=t.C,a=t.s,r=(this.props.checked?this.i:this.o)+e-n;t.R||e===n||this.setState({R:!0});var c=Math.min(this.i,Math.max(this.o,r));c!==a&&this.setState({s:c})},t.prototype.S=function(e){var t=this.state,n=t.s,a=t.R,r=t.m,c=this.props.checked,o=(this.i+this.o)/2,s=Date.now()-r;!a||s<250?this.T(e):c?o<n?this.setState({s:this.i}):this.T(e):n<o?this.setState({s:this.o}):this.T(e),this.setState({R:!1,M:!1}),this.n=Date.now()},t.prototype.h=function(e){e.preventDefault(),"number"==typeof e.button&&0!==e.button||(this.k(e.clientX),window.addEventListener("mousemove",this.r),window.addEventListener("mouseup",this.a))},t.prototype.r=function(e){e.preventDefault(),this.x(e.clientX)},t.prototype.a=function(e){this.S(e),window.removeEventListener("mousemove",this.r),window.removeEventListener("mouseup",this.a)},t.prototype.c=function(e){this.$=null,this.k(e.touches[0].clientX)},t.prototype.l=function(e){this.x(e.touches[0].clientX)},t.prototype.u=function(e){e.preventDefault(),this.S(e)},t.prototype.p=function(e){50<Date.now()-this.n&&(this.T(e),50<Date.now()-this.e&&this.setState({M:!1}))},t.prototype.b=function(){this.e=Date.now()},t.prototype.g=function(){this.setState({M:!0})},t.prototype.v=function(){this.setState({M:!1})},t.prototype.w=function(e){this.y=e},t.prototype.f=function(e){e.preventDefault(),this.y.focus(),this.T(e),this.setState({M:!1})},t.prototype.T=function(e){var t=this.props;(0,t.onChange)(!t.checked,e,t.id)},t.prototype.render=function(){var e=this.props,t=e.disabled,n=e.className,c=e.offColor,o=e.onColor,s=e.offHandleColor,u=e.onHandleColor,l=e.checkedIcon,p=e.uncheckedIcon,h=e.boxShadow,f=e.activeBoxShadow,d=e.height,m=e.width,b=function(e,t){var n={};for(var a in e)Object.prototype.hasOwnProperty.call(e,a)&&-1===t.indexOf(a)&&(n[a]=e[a]);return n}(e,["disabled","className","offColor","onColor","offHandleColor","onHandleColor","checkedIcon","uncheckedIcon","boxShadow","activeBoxShadow","height","width","handleDiameter"]),v=this.state,y=v.s,O=v.R,j=v.M,g={position:"relative",display:"inline-block",textAlign:"left",opacity:t?.5:1,direction:"ltr",borderRadius:d/2,WebkitTransition:"opacity 0.25s",MozTransition:"opacity 0.25s",transition:"opacity 0.25s",touchAction:"none",WebkitTapHighlightColor:"rgba(0, 0, 0, 0)",WebkitUserSelect:"none",MozUserSelect:"none",msUserSelect:"none",userSelect:"none"},x={height:d,width:m,margin:Math.max(0,(this.t-d)/2),position:"relative",background:i(y,this.i,this.o,c,o),borderRadius:d/2,cursor:t?"default":"pointer",WebkitTransition:O?null:"background 0.25s",MozTransition:O?null:"background 0.25s",transition:O?null:"background 0.25s"},w={height:d,width:Math.min(1.5*d,m-(this.t+d)/2+1),position:"relative",opacity:(y-this.o)/(this.i-this.o),pointerEvents:"none",WebkitTransition:O?null:"opacity 0.25s",MozTransition:O?null:"opacity 0.25s",transition:O?null:"opacity 0.25s"},E={height:d,width:Math.min(1.5*d,m-(this.t+d)/2+1),position:"absolute",opacity:1-(y-this.o)/(this.i-this.o),right:0,top:0,pointerEvents:"none",WebkitTransition:O?null:"opacity 0.25s",MozTransition:O?null:"opacity 0.25s",transition:O?null:"opacity 0.25s"},k={height:this.t,width:this.t,background:i(y,this.i,this.o,s,u),display:"inline-block",cursor:t?"default":"pointer",borderRadius:"50%",position:"absolute",transform:"translateX("+y+"px)",top:Math.max(0,(d-this.t)/2),outline:0,boxShadow:j?f:h,border:0,WebkitTransition:O?null:"background-color 0.25s, transform 0.25s, box-shadow 0.15s",MozTransition:O?null:"background-color 0.25s, transform 0.25s, box-shadow 0.15s",transition:O?null:"background-color 0.25s, transform 0.25s, box-shadow 0.15s"};return a.createElement("div",{className:n,style:g},a.createElement("div",{className:"react-switch-bg",style:x,onClick:t?null:this.f,onMouseDown:function(e){return e.preventDefault()}},l&&a.createElement("div",{style:w},l),p&&a.createElement("div",{style:E},p)),a.createElement("div",{className:"react-switch-handle",style:k,onClick:function(e){return e.preventDefault()},onMouseDown:t?null:this.h,onTouchStart:t?null:this.c,onTouchMove:t?null:this.l,onTouchEnd:t?null:this.u,onTouchCancel:t?null:this.v}),a.createElement("input",r({},{type:"checkbox",role:"switch",disabled:t,style:{border:0,clip:"rect(0 0 0 0)",height:1,margin:-1,overflow:"hidden",padding:0,position:"absolute",width:1}},b,{ref:this.w,onFocus:this.g,onBlur:this.v,onKeyUp:this.b,onChange:this.p})))},t}(a.Component);u.defaultProps={disabled:!1,offColor:"#888",onColor:"#080",offHandleColor:"#fff",onHandleColor:"#fff",uncheckedIcon:c,checkedIcon:o,boxShadow:null,activeBoxShadow:"0 0 2px 3px #3bf",height:28,width:56},t.default=u},296:function(e,t,n){"use strict";var a=n(6),r=n(8),c=n(11),o=n.n(c),s=n(0),i=n.n(s),u=n(19),l=["xl","lg","md","sm","xs"],p=i.a.forwardRef((function(e,t){var n=e.bsPrefix,c=e.className,s=e.noGutters,p=e.as,h=void 0===p?"div":p,f=Object(r.a)(e,["bsPrefix","className","noGutters","as"]),d=Object(u.b)(n,"row"),m=d+"-cols",b=[];return l.forEach((function(e){var t,n=f[e];delete f[e];var a="xs"!==e?"-"+e:"";null!=(t=null!=n&&"object"===typeof n?n.cols:n)&&b.push(""+m+a+"-"+t)})),i.a.createElement(h,Object(a.a)({ref:t},f,{className:o.a.apply(void 0,[c,d,s&&"no-gutters"].concat(b))}))}));p.displayName="Row",p.defaultProps={noGutters:!1},t.a=p},311:function(e,t,n){"use strict";n.d(t,"d",(function(){return s})),n.d(t,"a",(function(){return u})),n.d(t,"b",(function(){return i})),n.d(t,"e",(function(){return p})),n.d(t,"c",(function(){return l}));var a=n(20),r=n.n(a),c=n(33),o=n(47),s=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/sales/customers/get","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),i=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/sales/customers/delete","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),u=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/sales/customer/add","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),l=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/sales/customer/get","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),p=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/sales/customer/update","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}()},313:function(e,t,n){"use strict";var a=n(6),r=n(8),c=n(11),o=n.n(c),s=n(0),i=n.n(s),u=n(19),l=n(66),p=n(266),h=n(84),f=i.a.forwardRef((function(e,t){var n=e.bsPrefix,c=e.className,s=e.variant,l=e.as,p=void 0===l?"img":l,h=Object(r.a)(e,["bsPrefix","className","variant","as"]),f=Object(u.b)(n,"card-img");return i.a.createElement(p,Object(a.a)({ref:t,className:o()(s?f+"-"+s:f,c)},h))}));f.displayName="CardImg",f.defaultProps={variant:null};var d=f,m=Object(p.a)("h5"),b=Object(p.a)("h6"),v=Object(l.a)("card-body"),y=i.a.forwardRef((function(e,t){var n=e.bsPrefix,c=e.className,l=e.bg,p=e.text,f=e.border,d=e.body,m=e.children,b=e.as,y=void 0===b?"div":b,O=Object(r.a)(e,["bsPrefix","className","bg","text","border","body","children","as"]),j=Object(u.b)(n,"card"),g=Object(s.useMemo)((function(){return{cardHeaderBsPrefix:j+"-header"}}),[j]);return i.a.createElement(h.a.Provider,{value:g},i.a.createElement(y,Object(a.a)({ref:t},O,{className:o()(c,j,l&&"bg-"+l,p&&"text-"+p,f&&"border-"+f)}),d?i.a.createElement(v,null,m):m))}));y.displayName="Card",y.defaultProps={body:!1},y.Img=d,y.Title=Object(l.a)("card-title",{Component:m}),y.Subtitle=Object(l.a)("card-subtitle",{Component:b}),y.Body=v,y.Link=Object(l.a)("card-link",{Component:"a"}),y.Text=Object(l.a)("card-text",{Component:"p"}),y.Header=Object(l.a)("card-header"),y.Footer=Object(l.a)("card-footer"),y.ImgOverlay=Object(l.a)("card-img-overlay");t.a=y},431:function(e,t,n){"use strict";n.d(t,"d",(function(){return p})),n.d(t,"c",(function(){return s})),n.d(t,"a",(function(){return l})),n.d(t,"b",(function(){return i})),n.d(t,"e",(function(){return u}));var a=n(20),r=n.n(a),c=n(33),o=n(47),s=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/sales/customers/category","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),i=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/sales/customers/category/delete","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),u=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/sales/customers/category/update","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),l=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/sales/customers/category/add","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}(),p=function(){var e=Object(c.a)(r.a.mark((function e(t,n){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(o.a)("api/v1/sales/customers/category/get","POST",t,n);case 3:return e.abrupt("return",e.sent);case 6:e.prev=6,e.t0=e.catch(0),alert(e.t0);case 9:case"end":return e.stop()}}),e,null,[[0,6]])})));return function(t,n){return e.apply(this,arguments)}}()},451:function(e,t,n){"use strict";n.d(t,"a",(function(){return r}));var a=n(36),r=function(e){var t={};return Object(a.a)(e.fname)&&(t.fname="First Name cannot be empty."),Object(a.a)(e.lname)&&(t.lname="Last Name cannot be empty."),Object(a.a)(e.email)&&(t.email="Email cannot be empty."),e.email&&!/^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/.test(e.email)&&(t.email="Email not valid."),Object(a.a)(e.phone1)&&(t.phone1="Atleast, a phone number should be provided."),{isValid:Object(a.a)(t),errors:t}}}}]);
//# sourceMappingURL=46.98d32751.chunk.js.map