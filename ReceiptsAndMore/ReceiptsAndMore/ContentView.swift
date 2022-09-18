//
//  ContentView.swift
//  ReceiptsAndMore
//
//  Created by MacBookPro on 2022/9/16.
//

import SwiftUI
import UIKit
import Firebase

struct ContentView: View {
    @State private var email = ""
    @State private var password = ""
    @State private var userIsLoggedIn = false
    
    var body: some View {
        if userIsLoggedIn {
            content
        } else {
            content
        }
    }
    
    var content: some View {
        ZStack {
            Color.white
            RoundedRectangle(cornerRadius: 30, style: .continuous)
                .foregroundStyle(.linearGradient(colors: [.blue, .green], startPoint: .topLeading, endPoint: .bottomTrailing))
                .frame(width: 1000, height: 400)
                .rotationEffect(.degrees(135))
                //.offset(y: -350)
            //LinearGradient(gradient: Gradient(colors: [.green, .blue]), startPoint: .top, endPoint: .bottom)
            
            VStack(spacing: 20) {
                Spacer()
                Text("Welcome")
                    .foregroundColor(.white)
                    .font(.system(size: 35, weight: .bold))
                    //.offset(x: -70, y: -50)
                
                TextField("", text: $email)
                    .offset(x: 20, y: 20)
                    .foregroundColor(.white)
                    .textFieldStyle(.plain)
                    .placeholder(when: email.isEmpty) {
                        Text("Email")
                            .foregroundColor(.white)
                            .bold()
                            .offset(x: 25, y: 18)
                    }
                Rectangle()
                    .frame(width: 300, height: 1)
                    .foregroundColor(.white)
                
                SecureField("", text: $password)
                    .offset(x: 20, y: 20)
                    .foregroundColor(.white)
                    .textFieldStyle(.plain)
                    .placeholder(when: password.isEmpty) {
                        Text("Password")
                            .foregroundColor(.white)
                            .bold()
                            .offset(x: 25, y: 18)
                    }
                
                Rectangle()
                    .frame(width: 300, height: 1)
                    .foregroundColor(.white)
                
                Button {
                    register()
                } label: {
                    Text("Sign Up")
                        .bold()
                        .frame(width: 150, height: 35)
                        .background(
                            RoundedRectangle(cornerRadius: 10, style: .continuous)
                                .fill(.linearGradient(colors: [.blue, .green], startPoint: .topLeading, endPoint: .bottomTrailing)))
                        .foregroundColor(.white)
                }
                 
                
                
                Button {
                    login()
                } label: {
                    Text("Already have an account? Log in")
                        .bold()
                        .foregroundColor(.white)
                        .font(.system(size: 15))
                }
                
                
                .padding(.top)
                
                
                Spacer()
            }
            .frame(width: 350)
            .onAppear {
                Auth.auth().addStateDidChangeListener { auth, user in
                    if user != nil {
                        userIsLoggedIn.toggle()
                    } else {
                        
                    }
                    
                }
            }
        }
        .ignoresSafeArea()
    }
    
    func login() { //can get user's account data from the object that's passed to the callback method
        Auth.auth().signIn(withEmail: email, password: password) { result, error in
            if error != nil {
                print(error!.localizedDescription)
            } else {
                // idk
            }
                
            }
        }
        /* if Auth.auth().currentUser != nil {
         let user = Auth.auth().currentUser
         if let user = user {
             let uid = user.uid
             let email = user.email
         }
     } else {
         // no user is signed in
     }*/
    //}
    
    func register() {
        Auth.auth().createUser(withEmail: email, password: password) { result, error in
            if error != nil {
                print(error!.localizedDescription)
            }
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}

extension View {
    func placeholder<Content: View>(
        when shouldShow: Bool,
        alignment: Alignment = .leading,
        @ViewBuilder placeholder: () -> Content) -> some View {

        ZStack(alignment: alignment) {
            placeholder().opacity(shouldShow ? 1 : 0)
            self
        }
    }
}
