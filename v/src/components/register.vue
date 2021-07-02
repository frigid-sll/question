<template>
	<div id="reg" class="container"> 
		<form role="form"  v-on:submit.prevent='reg'>
			<div class="form-group col-xs-8 col-xs-offset-2">
				<h2 class="text-center"><i>Register User</i></h2><br><br>
				<input type="text" name="account" placeholder="请输入账号" class="form-control" v-model='account'><br>
				<input type="password" name="password" placeholder="请输入密码" class="form-control"  v-model='password'><br>
                <select class="form-control" id="sex">
                    <option value="男" selected>男</option>
                    <option value="女">女</option>
                </select>
				<br>
				<button class="btn btn-success  col-md-4 col-md-offset-4">Register</button><br>
				<a class="col-md-4 col-md-offset-4" @click='login'>login</a>
			</div>
		</form>
	</div>
</template>
<script type="text/javascript">
	import Qs from 'qs'
	export default{
		data:function(){
			return{
				account:'',
				password:'',
                sex:''
			}
		},
		methods:{
			reg:function(){
                this.sex=document.getElementById('sex').value
				this.axios.post('/api/user/register/',
					Qs.stringify({  
               			account: this.account,
               			password:this.password,
                        sex:this.sex
            		}),
					{headers: {'X-CSRFToken': this.getCookie('csrftoken')}}
					).then((res)=>{
						if(res.data.code==200){
                            alert('注册成功')
                            parent.location.reload()
						}else{
							alert('注册失败，该账号已存在')
						}		
					}).catch(function(error){
						console.log(error)
					})
			},
			login:function(){
				this.$router.replace('/login')
			},
			getCookie(name) {
                var value = '; ' + document.cookie;
                var parts = value.split('; ' + name + '=');
                if (parts.length === 2) return parts.pop().split(';').shift()
            },
		}
	}
</script>