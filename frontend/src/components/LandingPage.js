import React, { useState } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { useToast } from '../hooks/use-toast';
import { 
  Music, 
  Shield, 
  Zap, 
  Radio, 
  Coins, 
  Twitter, 
  MessageCircle, 
  Instagram, 
  Github,
  Mail,
  Heart,
  ArrowRight
} from 'lucide-react';
import { features, socialLinks, kofiUrl, mockEmailSignup } from '../mock';

const iconMap = {
  Music,
  Shield, 
  Zap,
  Radio,
  Coins,
  Twitter,
  MessageCircle,
  Instagram,
  Github
};

const LandingPage = () => {
  const [email, setEmail] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { toast } = useToast();

  const handleEmailSubmit = async (e) => {
    e.preventDefault();
    if (!email) {
      toast({
        title: "Error",
        description: "Please enter your email address",
        variant: "destructive"
      });
      return;
    }

    setIsSubmitting(true);
    try {
      const result = await mockEmailSignup(email);
      toast({
        title: "Success!",
        description: result.message,
        variant: "default"
      });
      setEmail('');
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to join waitlist. Please try again.",
        variant: "destructive"
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const FeatureIcon = ({ iconName, className }) => {
    const Icon = iconMap[iconName];
    return Icon ? <Icon className={className} /> : null;
  };

  return (
    <div className="min-h-screen bg-black text-par-green">
      {/* Header */}
      <header className="text-center py-12 px-4">
        <div className="max-w-4xl mx-auto">
          <img 
            src="https://customer-assets.emergentagent.com/job_7593d419-9ab6-4246-b323-b30045671f1d/artifacts/1lf12na8_IQ_Coded%282%29.png" 
            alt="P.A.R. Logo" 
            className="max-w-[300px] w-full mx-auto mb-6 filter brightness-110 drop-shadow-[0_0_20px_rgba(57,255,20,0.3)]"
          />
          <h1 className="font-orbitron text-4xl md:text-5xl lg:text-6xl font-bold mb-4 text-shadow-glow">
            Post Apocalyptic Radio
          </h1>
          <h2 className="font-orbitron text-xl md:text-2xl mb-2 text-par-green-light">
            (P.A.R.)
          </h2>
          <p className="font-tech text-lg md:text-xl italic text-par-green-dim">
            Your Decentralized, Social Music Frontier
          </p>
        </div>
      </header>

      {/* Introduction */}
      <section className="max-w-4xl mx-auto px-4 mb-12">
        <p className="font-tech text-base md:text-lg leading-relaxed text-center">
          Imagine a world where music isn't controlled by a few central platforms, but by the artists and communities who love it. 
          That's the vision behind <strong className="text-par-green-bright">Post Apocalyptic Radio (P.A.R.)</strong> – 
          a new kind of music streaming experience built for the decentralized future.
        </p>
      </section>

      {/* Features Grid */}
      <section className="max-w-6xl mx-auto px-4 mb-16">
        <h2 className="font-orbitron text-3xl md:text-4xl font-bold text-center mb-12 text-shadow-glow">
          What Makes P.A.R. Unique?
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => (
            <Card 
              key={feature.id} 
              className="par-card group hover:scale-[1.02] transition-all duration-300 hover:shadow-par-glow"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <CardHeader className="pb-4">
                <div className="flex items-center gap-3 mb-2">
                  <div className="p-2 rounded-lg bg-par-green/10 group-hover:bg-par-green/20 transition-colors">
                    <FeatureIcon iconName={feature.icon} className="w-6 h-6 text-par-green" />
                  </div>
                  <CardTitle className="font-orbitron text-lg text-par-green group-hover:text-par-green-bright transition-colors">
                    {feature.title}
                  </CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <CardDescription className="font-tech text-par-green-dim text-sm leading-relaxed">
                  {feature.description}
                </CardDescription>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      {/* CTA Section */}
      <section className="max-w-2xl mx-auto px-4 mb-16">
        <div className="par-card p-8 text-center">
          <h2 className="font-orbitron text-2xl md:text-3xl font-bold mb-4 text-shadow-glow">
            Join the Revolution
          </h2>
          <p className="font-tech text-par-green-dim mb-8">
            Be among the first to experience the future of decentralized music streaming. 
            Sign up for early beta access and help shape the soundtrack of tomorrow.
          </p>
          
          <form onSubmit={handleEmailSubmit} className="flex flex-col sm:flex-row gap-4 mb-6">
            <Input
              type="email"
              placeholder="Enter your email address"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="par-input flex-1"
            />
            <Button 
              type="submit" 
              disabled={isSubmitting}
              className="par-button group"
            >
              {isSubmitting ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-black mr-2"></div>
                  Joining...
                </>
              ) : (
                <>
                  <Mail className="w-4 h-4 mr-2" />
                  Join Beta
                  <ArrowRight className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" />
                </>
              )}
            </Button>
          </form>

          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <span className="font-tech text-par-green-dim">or</span>
            <Button 
              variant="outline" 
              asChild
              className="par-button-outline group"
            >
              <a href={kofiUrl} target="_blank" rel="noopener noreferrer">
                <Heart className="w-4 h-4 mr-2 group-hover:text-red-500 transition-colors" />
                Support on Ko-fi
              </a>
            </Button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-par-green/20 py-12 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <h3 className="font-orbitron text-xl font-bold mb-6 text-shadow-glow">
            Follow the Signal
          </h3>
          <div className="flex justify-center gap-6 mb-8">
            {socialLinks.map((social) => (
              <a
                key={social.name}
                href={social.url}
                target="_blank"
                rel="noopener noreferrer"
                className="p-3 rounded-lg border border-par-green/30 hover:border-par-green hover:bg-par-green/10 transition-all duration-300 hover:scale-110 hover:shadow-par-glow group"
                aria-label={social.name}
              >
                <FeatureIcon iconName={social.icon} className="w-6 h-6 text-par-green group-hover:text-par-green-bright transition-colors" />
              </a>
            ))}
          </div>
          <p className="font-tech text-sm text-par-green-dim">
            P.A.R. © 2025 - Building the Future of Decentralized Music
          </p>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;