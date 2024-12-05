declare module 'react-facebook-login' {
  interface ReactFacebookLoginInfo {
    accessToken: string;
    userID: string;
    expiresIn: number;
    signedRequest: string;
    email?: string;
    name?: string;
    picture?: {
      data: {
        height: number;
        is_silhouette: boolean;
        url: string;
        width: number;
      };
    };
  }

  interface ReactFacebookFailureResponse {
    status?: string;
  }

  interface ReactFacebookLoginProps {
    appId: string;
    callback(response: ReactFacebookLoginInfo | ReactFacebookFailureResponse): void;
    onFailure?(response: ReactFacebookFailureResponse): void;
    autoLoad?: boolean;
    fields?: string;
    scope?: string;
    xfbml?: boolean;
    cookie?: boolean;
    textButton?: string;
    typeButton?: string;
    cssClass?: string;
    version?: string;
    language?: string;
    onClick?(): void;
    containerStyle?: React.CSSProperties;
    icon?: React.ReactNode;
    render?(props: { onClick: () => void }): JSX.Element;
  }

  const ReactFacebookLogin: React.ComponentType<ReactFacebookLoginProps>;

  export default ReactFacebookLogin;
}
