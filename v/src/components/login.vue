<template>
    <div id="Login" class="container">
        {{get_question_classify}}{{is_login}}{{_path}}
        <form role="form" v-on:submit.prevent='login'>
			<div class="form-group col-xs-8 col-xs-offset-2">
				<h2 class="text-center"><i>Login User</i></h2><br><br>
				<input type="text" name="account" v-model='account' class="form-control" placeholder="请输入账号"><br>
				<input type="password" name="password" v-model='password' class="form-control" placeholder="请输入密码"><br>
                <select class="form-control" id="classify">
                    <option v-for="x in all_question_classify" :value="x.class_name" selected>{{x.class_name}}</option>
                </select>
                <br>
				<button class="btn btn-success   col-md-4 col-md-offset-4" >sign in</button><p>
				<a class="col-md-4 col-md-offset-4" @click='register'>Register</a></p>
			</div>
		</form>
    </div>
</template>
<script>
import Qs from 'qs'
export default {
    data(){
        return{
            account:'',
            password:'',
            question_classify:'',
            all_question_classify:'',
            root:''
        }
    },
    computed:{
        get_question_classify:function(){
            this.axios.get('/api/acquire/question_classify/').then((res)=>{
					if(res.data.code==200){
						this.all_question_classify=res.data.res
					}
					}).catch(function(error){
						console.log(error)
					})
        },
        is_login:function(){
            if(localStorage.getItem("account")){
                this.$router.push({
                        path:localStorage.getItem("path"),
                    })
            }
        },
        _path:function(){
            localStorage.setItem('path','/login')
        }
        
    },
    methods:{
        login:function(){
            this.question_classify=document.getElementById('classify').value
            this.axios.post('/api/user/login/',
                            Qs.stringify({  
                                account:this.account,
                                password:this.password
                            }),
                            {headers: {'X-CSRFToken': this.getCookie('csrftoken')}}
                            ).then((res)=>{
                                if(res.data.code==200){
                                    localStorage.setItem('account',this.account)
                                    localStorage.setItem('question_classify',this.question_classify)
                                    localStorage.setItem('sex',res.data.sex)
                                    this.root=res.data.root
                                    if(this.root==0){
                                        this.$router.push({
                                            path:'/catalogue',
                                        })
                                    }else{
                                        localStorage.setItem('root',this.account)
                                        this.$router.push({
                                            path:'/root',
                                        })
                                    }
                                    
                                }else{
                                    alert('登录失败')
                                }
                            })
        },
        register:function(){
            this.$router.replace('/register')
        },
        getCookie(name) {
                var value = '; ' + document.cookie;
                var parts = value.split('; ' + name + '=');
                if (parts.length === 2) return parts.pop().split(';').shift()
            },
    }
}
</script>