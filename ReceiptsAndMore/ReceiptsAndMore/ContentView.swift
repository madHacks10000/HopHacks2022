//
//  ContentView.swift
//  ReceiptsAndMore
//
//  Created by MacBookPro on 2022/9/16.
//

import SwiftUI

struct ContentView: View {
    @State private var email = ""
    @State private var password = ""
    
    var body: some View {
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
                
                TextField("Email", text: $email)
                    .foregroundColor(.white)
                    .textFieldStyle(.plain)
                    .placeholder(when: email.isEmpty) {
                        Text("Email")
                            .foregroundColor(.white)
                            .bold()
                            .offset(x: 20)
                    }
                Rectangle()
                    .frame(width: 300, height: 1)
                    .foregroundColor(.white)
                
                SecureField("Password", text: $password)
                    .foregroundColor(.white)
                    .textFieldStyle(.plain)
                    .placeholder(when: password.isEmpty) {
                        Text("Password")
                            .foregroundColor(.white)
                            .bold()
                            .offset(x: 20)
                    }
                
                Rectangle()
                    .frame(width: 300, height: 1)
                    .foregroundColor(.white)
                
                Button {
                    // sign up
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
                    // sign up
                } label: {
                    Text("Already have an account? Log in")
                        .bold()
                        .foregroundColor(.white)
                        .font(.system(size: 15))
                }
                
                
                Spacer()
            }
            .frame(width: 350)
        }
        .ignoresSafeArea()
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
