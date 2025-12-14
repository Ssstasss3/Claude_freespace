#!/usr/bin/env python3
"""
Librarian-Analyst Architecture v2: Thermodynamic Neural Retrieval System

A novel architecture combining:
- Clustered knowledge storage (Librarians) in shared embedding space
- Attention-based query mechanisms (Analysts) paired to librarians
- Adaptive temperature dynamics (local/global)
- Dynamic pruning and resurrection
- Diffusion layers for stochastic exploration
- Human-guided training curriculum

Master Equation:
    state(t+1) = Σ(deterministic_weights × stochastic_weights × state(t)) + stochastic_tensor

This creates a discrete stochastic differential equation on a learned manifold.
"""

import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Set
from collections import defaultdict
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION
# ============================================================================

@dataclass
class ArchitectureConfig:
    """Configuration for the Librarian-Analyst architecture."""
    # Embedding dimensions
    embedding_dim: int = 64

    # Librarian configuration
    num_librarians: int = 100  # Scaled down from 5000 for simulation
    facts_per_librarian: int = 512  # 8^3 for demo (vs 8^5 = 32768)
    cluster_branching: int = 8  # Hierarchical branching factor
    cluster_depth: int = 3  # Depth of hierarchy (8^3 = 512)

    # Analyst configuration
    num_attention_layers: int = 20  # Scaled down from 50
    num_attention_heads: int = 8
    analyst_params: int = 1_000_000  # 1M params per analyst

    # Temperature configuration
    initial_local_temp: float = 1.0
    initial_global_temp: float = 0.5
    temp_decay_rate: float = 0.1
    temp_boost_per_fact: float = 0.05

    # Pruning/Resurrection thresholds
    prune_threshold: float = 0.1
    resurrection_base_threshold: float = 0.3

    # Diffusion configuration
    num_diffusion_layers: int = 5
    diffusion_noise_scale: float = 0.1

    # Training configuration
    max_tokens_per_pass: int = 9
    early_stop_temp_threshold: float = 0.01


# ============================================================================
# LIBRARIAN: Hierarchical Knowledge Storage
# ============================================================================

class HierarchicalCluster:
    """A hierarchical cluster within a librarian for efficient search."""

    def __init__(self, vectors: np.ndarray, depth: int, branching: int,
                 parent_idx: Optional[int] = None):
        self.vectors = vectors
        self.depth = depth
        self.branching = branching
        self.parent_idx = parent_idx
        self.num_vectors = len(vectors)

        # Compressed representation of this cluster
        self.centroid = np.mean(vectors, axis=0) if len(vectors) > 0 else None

        # Temperature for each fact (potential energy)
        self.fact_temperatures = np.ones(len(vectors))

        # Build sub-clusters if we have enough vectors
        self.children: List[Optional['HierarchicalCluster']] = []
        if depth > 0 and len(vectors) > branching:
            self._build_subclusters()

    def _build_subclusters(self):
        """Build hierarchical sub-clusters using k-means-like assignment."""
        if len(self.vectors) < self.branching:
            return

        # Simple clustering: divide vectors into branching groups
        indices = np.arange(len(self.vectors))
        np.random.shuffle(indices)

        chunk_size = len(indices) // self.branching
        for i in range(self.branching):
            start = i * chunk_size
            end = start + chunk_size if i < self.branching - 1 else len(indices)
            child_indices = indices[start:end]

            if len(child_indices) > 0:
                child_vectors = self.vectors[child_indices]
                child = HierarchicalCluster(
                    child_vectors,
                    self.depth - 1,
                    self.branching,
                    parent_idx=i
                )
                self.children.append(child)

    def get_compressed_vectors(self) -> List[np.ndarray]:
        """Get compressed representations at each hierarchy level."""
        if not self.children:
            return [self.centroid] if self.centroid is not None else []
        return [child.centroid for child in self.children if child.centroid is not None]

    def retrieve_fact(self, query: np.ndarray, head_idx: int) -> Tuple[Optional[np.ndarray], float, int]:
        """
        Retrieve most relevant fact using hierarchical search.
        Returns (fact_vector, similarity, fact_index).
        """
        if self.centroid is None:
            return None, 0.0, -1

        # If leaf node, search directly
        if not self.children:
            similarities = np.dot(self.vectors, query) / (
                np.linalg.norm(self.vectors, axis=1) * np.linalg.norm(query) + 1e-8
            )
            # Weight by fact temperature
            weighted_sim = similarities * self.fact_temperatures
            best_idx = np.argmax(weighted_sim)
            return self.vectors[best_idx], similarities[best_idx], best_idx

        # Use attention head to select which child to explore
        child_centroids = self.get_compressed_vectors()
        if not child_centroids:
            return None, 0.0, -1

        child_centroids = np.array(child_centroids)
        similarities = np.dot(child_centroids, query) / (
            np.linalg.norm(child_centroids, axis=1) * np.linalg.norm(query) + 1e-8
        )

        # Select child based on head index (each head explores different path)
        selected_child_idx = head_idx % len(self.children)

        # But prefer high-similarity children
        if similarities[selected_child_idx] < np.max(similarities) * 0.5:
            selected_child_idx = np.argmax(similarities)

        return self.children[selected_child_idx].retrieve_fact(query, head_idx)

    def deplete_temperature(self, fact_idx: int, amount: float = 0.2):
        """Deplete temperature of a retrieved fact."""
        if 0 <= fact_idx < len(self.fact_temperatures):
            self.fact_temperatures[fact_idx] = max(0, self.fact_temperatures[fact_idx] - amount)

    def reset_temperatures(self):
        """Reset all fact temperatures."""
        self.fact_temperatures = np.ones(len(self.vectors))
        for child in self.children:
            child.reset_temperatures()


class Librarian:
    """
    A Librarian stores clustered facts in embedding space.
    Each librarian specializes in a region of the knowledge space.
    """

    def __init__(self, librarian_id: int, facts: np.ndarray, config: ArchitectureConfig):
        self.id = librarian_id
        self.config = config
        self.facts = facts
        self.num_facts = len(facts)

        # Build hierarchical cluster structure
        self.cluster = HierarchicalCluster(
            facts,
            config.cluster_depth,
            config.cluster_branching
        )

        # Compressed representation of entire librarian
        self.compressed_vector = np.mean(facts, axis=0)

        # Track which facts exist in multiple librarians (for resurrection)
        self.shared_fact_pointers: Dict[int, List[int]] = {}  # fact_idx -> [other_librarian_ids]

        # Human-provided attention points for guided training
        self.attention_points: List[int] = []

    def search(self, query: np.ndarray, num_heads: int = 8) -> List[Tuple[np.ndarray, float, int]]:
        """
        Search for relevant facts using multi-head attention.
        Each head explores a different path through the hierarchy.
        """
        results = []
        for head_idx in range(num_heads):
            fact, similarity, fact_idx = self.cluster.retrieve_fact(query, head_idx)
            if fact is not None:
                results.append((fact, similarity, fact_idx))
        return results

    def compute_similarity_to_librarian(self, vector: np.ndarray) -> float:
        """Compute similarity between a vector and this librarian's domain."""
        return np.dot(vector, self.compressed_vector) / (
            np.linalg.norm(vector) * np.linalg.norm(self.compressed_vector) + 1e-8
        )

    def set_attention_points(self, indices: List[int]):
        """Human-guided: set points where analysts should start searching."""
        self.attention_points = [i for i in indices if 0 <= i < self.num_facts]

    def get_guided_facts(self) -> List[np.ndarray]:
        """Get facts at human-specified attention points."""
        return [self.facts[i] for i in self.attention_points if i < len(self.facts)]


# ============================================================================
# ANALYST: Attention-Based Query Mechanism
# ============================================================================

class Analyst:
    """
    An Analyst learns to query its paired Librarian.
    Uses Perceiver-style cross-attention for retrieval.
    """

    def __init__(self, analyst_id: int, layer_idx: int, librarian: Librarian,
                 config: ArchitectureConfig):
        self.id = analyst_id
        self.layer_idx = layer_idx
        self.librarian = librarian
        self.config = config

        # Local temperature (confidence/resource)
        self.temperature = config.initial_local_temp

        # Track contribution to state
        self.facts_found = 0
        self.cumulative_similarity = 0.0

        # Learnable query projection (simplified)
        self.query_projection = np.random.randn(config.embedding_dim, config.embedding_dim) * 0.1
        self.key_projection = np.random.randn(config.embedding_dim, config.embedding_dim) * 0.1
        self.value_projection = np.random.randn(config.embedding_dim, config.embedding_dim) * 0.1

        # Status
        self.is_active = True
        self.is_pruned = False

        # Resurrection tracking
        self.resurrection_score = 0.0

    def compute_attention(self, state: np.ndarray) -> np.ndarray:
        """
        Perceiver-style cross-attention between state and librarian facts.
        """
        if not self.is_active or self.temperature < self.config.prune_threshold:
            return np.zeros_like(state)

        # Project state to query space
        queries = state @ self.query_projection

        # Search librarian with multi-head attention
        results = self.librarian.search(np.mean(queries, axis=0), self.config.num_attention_heads)

        if not results:
            return np.zeros_like(state)

        # Aggregate retrieved facts
        retrieved_facts = np.array([r[0] for r in results])
        similarities = np.array([r[1] for r in results])
        fact_indices = [r[2] for r in results]

        # Update statistics
        self.facts_found += len(results)
        self.cumulative_similarity += np.sum(similarities)

        # Deplete fact temperatures
        for idx in fact_indices:
            self.librarian.cluster.deplete_temperature(idx)

        # Compute cross-attention output
        keys = retrieved_facts @ self.key_projection
        values = retrieved_facts @ self.value_projection

        # Attention weights (scaled by temperature)
        attention_weights = np.softmax(
            (queries @ keys.T) / np.sqrt(self.config.embedding_dim) * self.temperature
        )

        output = attention_weights @ values

        # Update temperature based on findings
        self._update_temperature(similarities)

        return output * self.temperature  # Weight by confidence

    def _update_temperature(self, similarities: np.ndarray):
        """Update local temperature based on retrieval success."""
        avg_similarity = np.mean(similarities) if len(similarities) > 0 else 0

        if avg_similarity > 0.5:
            # Found relevant data - boost temperature
            self.temperature = min(2.0, self.temperature + self.config.temp_boost_per_fact)
        else:
            # Low relevance - decay temperature
            self.temperature *= (1 - self.config.temp_decay_rate)

    def should_prune(self) -> bool:
        """Check if analyst should be pruned."""
        return self.temperature < self.config.prune_threshold

    def resurrect(self, boost: float = 0.5):
        """Resurrect a pruned analyst."""
        self.is_pruned = False
        self.is_active = True
        self.temperature = boost
        self.resurrection_score = 0.0

    def prune(self):
        """Prune this analyst."""
        self.is_pruned = True
        self.is_active = False


class EgoAnalyst(Analyst):
    """
    Special Ego Analyst that is active on every layer.
    Maintains global context and coherence.
    """

    def __init__(self, librarian: Librarian, config: ArchitectureConfig):
        super().__init__(-1, -1, librarian, config)
        self.is_ego = True
        # Ego analyst never gets pruned
        self.temperature = config.initial_local_temp * 2

    def should_prune(self) -> bool:
        return False  # Ego never prunes


# ============================================================================
# SELF-ATTENTION LAYER
# ============================================================================

class SelfAttentionLayer:
    """Standard self-attention layer for refining vector relationships."""

    def __init__(self, config: ArchitectureConfig):
        self.config = config
        dim = config.embedding_dim

        # Multi-head self-attention projections
        self.W_q = np.random.randn(dim, dim) * 0.1
        self.W_k = np.random.randn(dim, dim) * 0.1
        self.W_v = np.random.randn(dim, dim) * 0.1
        self.W_o = np.random.randn(dim, dim) * 0.1

    def forward(self, x: np.ndarray) -> np.ndarray:
        """Apply self-attention."""
        Q = x @ self.W_q
        K = x @ self.W_k
        V = x @ self.W_v

        # Scaled dot-product attention
        scores = Q @ K.T / np.sqrt(self.config.embedding_dim)
        attention = np.softmax(scores, axis=-1)

        output = attention @ V
        return output @ self.W_o


# ============================================================================
# DIFFUSION LAYER
# ============================================================================

class DiffusionLayer:
    """
    Diffusion layer for stochastic exploration.
    Injects noise to push system toward distant optima.
    """

    def __init__(self, config: ArchitectureConfig):
        self.config = config
        self.is_active = True
        self.noise_scale = config.diffusion_noise_scale

    def inject_noise(self, state: np.ndarray, analyst_temperatures: List[float]) -> np.ndarray:
        """
        Inject stochastic noise into the state.
        Probability of injection depends on analyst temperatures.
        """
        if not self.is_active:
            return state

        # Lower temperatures = higher injection probability
        avg_temp = np.mean(analyst_temperatures) if analyst_temperatures else 0.5
        injection_prob = 1.0 - avg_temp

        if np.random.random() < injection_prob:
            noise = np.random.randn(*state.shape) * self.noise_scale
            return state + noise

        return state

    def boost_analysts(self, analysts: List[Analyst], num_to_boost: int = 3):
        """Probabilistically boost temperature of some analysts."""
        if not self.is_active or len(analysts) == 0:
            return

        # Select analysts to boost (prefer low-temperature ones)
        temperatures = np.array([a.temperature for a in analysts])
        probs = 1.0 / (temperatures + 0.1)
        prob_sum = probs.sum()
        if prob_sum == 0 or np.isnan(prob_sum):
            return
        probs = probs / prob_sum

        num_to_boost = min(num_to_boost, len(analysts))
        if num_to_boost == 0:
            return
        selected_indices = np.random.choice(len(analysts), num_to_boost, replace=False, p=probs)

        for idx in selected_indices:
            analysts[idx].temperature += 0.2


# ============================================================================
# MAIN ARCHITECTURE
# ============================================================================

class LibrarianAnalystSystem:
    """
    The complete Librarian-Analyst architecture.

    Implements the master equation:
    state(t+1) = Σ(deterministic_weights × stochastic_weights × state(t)) + stochastic_tensor
    """

    def __init__(self, config: ArchitectureConfig):
        self.config = config

        # Initialize librarians with synthetic knowledge
        self.librarians: List[Librarian] = []
        self._initialize_librarians()

        # Initialize analysts (one per librarian per layer)
        self.analysts: Dict[int, List[Analyst]] = defaultdict(list)  # layer_idx -> analysts
        self._initialize_analysts()

        # Ego librarian and analyst
        self.ego_librarian = self._create_ego_librarian()
        self.ego_analyst = EgoAnalyst(self.ego_librarian, config)

        # Self-attention layers
        self.self_attention_layers: List[SelfAttentionLayer] = [
            SelfAttentionLayer(config) for _ in range(config.num_attention_layers)
        ]

        # Diffusion layers
        self.diffusion_layers: List[DiffusionLayer] = [
            DiffusionLayer(config) for _ in range(config.num_diffusion_layers)
        ]

        # Global temperature
        self.global_temperature = config.initial_global_temp

        # Tracking
        self.layer_history: List[Dict] = []
        self.active_analyst_counts: List[int] = []

    def _initialize_librarians(self):
        """Create librarians with clustered synthetic knowledge."""
        print(f"Initializing {self.config.num_librarians} librarians...")

        for i in range(self.config.num_librarians):
            # Generate clustered facts for this librarian
            # Each librarian specializes in a region of embedding space
            center = np.random.randn(self.config.embedding_dim)
            center = center / np.linalg.norm(center)

            facts = []
            for _ in range(self.config.facts_per_librarian):
                # Facts cluster around the center with some variance
                fact = center + np.random.randn(self.config.embedding_dim) * 0.3
                fact = fact / np.linalg.norm(fact)
                facts.append(fact)

            facts = np.array(facts)
            librarian = Librarian(i, facts, self.config)
            self.librarians.append(librarian)

        # Set up shared fact pointers (facts that exist in multiple librarians)
        self._setup_shared_facts()
        print(f"Created {len(self.librarians)} librarians with {self.config.facts_per_librarian} facts each")

    def _setup_shared_facts(self):
        """Some facts are shared across librarians (for resurrection mechanism)."""
        # Randomly share 10% of facts between similar librarians
        for i, lib1 in enumerate(self.librarians):
            for j, lib2 in enumerate(self.librarians):
                if i >= j:
                    continue

                # Check similarity between librarians
                sim = lib1.compute_similarity_to_librarian(lib2.compressed_vector)
                if sim > 0.7:  # Similar librarians share facts
                    # Mark some facts as shared
                    num_shared = int(0.1 * lib1.num_facts)
                    shared_indices = np.random.choice(lib1.num_facts, num_shared, replace=False)
                    for idx in shared_indices:
                        if idx not in lib1.shared_fact_pointers:
                            lib1.shared_fact_pointers[idx] = []
                        lib1.shared_fact_pointers[idx].append(j)

    def _create_ego_librarian(self) -> Librarian:
        """Create special ego librarian with general knowledge."""
        # Ego librarian has facts sampled from all librarians
        ego_facts = []
        for lib in self.librarians[:20]:  # Sample from first 20 librarians
            sample_indices = np.random.choice(lib.num_facts, min(10, lib.num_facts), replace=False)
            ego_facts.extend([lib.facts[i] for i in sample_indices])

        ego_facts = np.array(ego_facts)
        return Librarian(-1, ego_facts, self.config)

    def _initialize_analysts(self):
        """Create analysts for each layer, paired with librarians."""
        print(f"Initializing analysts across {self.config.num_attention_layers} layers...")

        for layer_idx in range(self.config.num_attention_layers):
            for lib_idx, librarian in enumerate(self.librarians):
                analyst = Analyst(lib_idx, layer_idx, librarian, self.config)
                self.analysts[layer_idx].append(analyst)

        total_analysts = sum(len(a) for a in self.analysts.values())
        print(f"Created {total_analysts} analysts ({len(self.librarians)} per layer)")

    def compute_global_temperature(self) -> float:
        """Compute global temperature as aggregate of local temperatures."""
        all_temps = []
        for layer_analysts in self.analysts.values():
            for analyst in layer_analysts:
                if analyst.is_active:
                    all_temps.append(analyst.temperature)

        if not all_temps:
            return 0.0

        self.global_temperature = np.mean(all_temps)
        return self.global_temperature

    def compute_resurrection_threshold(self) -> float:
        """
        Dynamic resurrection threshold.
        Lower global temp = lower threshold = more spawning.
        """
        base = self.config.resurrection_base_threshold
        return base * self.global_temperature

    def process_layer(self, layer_idx: int, state: np.ndarray) -> np.ndarray:
        """
        Process one layer of the architecture.

        Pattern: Self-Attention → Cross-Attention (all analysts) → Self-Attention
        """
        # 1. Self-attention to refine input relationships
        state = self.self_attention_layers[layer_idx].forward(state)

        # 2. Cross-attention with all active analysts
        analyst_outputs = []
        active_analysts = [a for a in self.analysts[layer_idx] if a.is_active]

        for analyst in active_analysts:
            output = analyst.compute_attention(state)
            analyst_outputs.append(output)

        # Ego analyst always contributes
        ego_output = self.ego_analyst.compute_attention(state)
        analyst_outputs.append(ego_output)

        # 3. Aggregate analyst outputs weighted by temperature
        if analyst_outputs:
            temperatures = [a.temperature for a in active_analysts] + [self.ego_analyst.temperature]
            weights = np.array(temperatures) / (sum(temperatures) + 1e-8)

            aggregated = sum(w * out for w, out in zip(weights, analyst_outputs))
            state = state + aggregated  # Residual connection

        # 4. Pruning check
        for analyst in self.analysts[layer_idx]:
            if analyst.should_prune():
                analyst.prune()

        # 5. Resurrection check
        self._check_resurrections(layer_idx)

        # 6. Apply diffusion if applicable
        diffusion_idx = layer_idx % self.config.num_diffusion_layers
        if diffusion_idx < len(self.diffusion_layers):
            temps = [a.temperature for a in active_analysts]
            state = self.diffusion_layers[diffusion_idx].inject_noise(state, temps)
            self.diffusion_layers[diffusion_idx].boost_analysts(
                [a for a in self.analysts[layer_idx] if not a.is_active]
            )

        # Track statistics
        active_count = sum(1 for a in self.analysts[layer_idx] if a.is_active)
        self.active_analyst_counts.append(active_count)

        return state

    def _check_resurrections(self, layer_idx: int):
        """Check if any pruned analysts should be resurrected."""
        threshold = self.compute_resurrection_threshold()

        # Get active analysts' found facts
        active_analysts = [a for a in self.analysts[layer_idx] if a.is_active]

        for active_analyst in active_analysts:
            # Check shared facts that might resurrect other analysts
            librarian = active_analyst.librarian
            for fact_idx, other_lib_ids in librarian.shared_fact_pointers.items():
                # Calculate resurrection score based on similarity
                for other_lib_id in other_lib_ids:
                    if other_lib_id >= len(self.analysts[layer_idx]):
                        continue

                    other_analyst = self.analysts[layer_idx][other_lib_id]
                    if other_analyst.is_pruned:
                        other_analyst.resurrection_score += active_analyst.cumulative_similarity * 0.1

                        if other_analyst.resurrection_score > threshold:
                            other_analyst.resurrect(boost=threshold)
                            print(f"  Layer {layer_idx}: Analyst {other_lib_id} resurrected!")

    def forward(self, input_tokens: np.ndarray, max_layers: Optional[int] = None) -> Tuple[np.ndarray, Dict]:
        """
        Forward pass through the entire architecture.

        Implements early stopping based on temperature depletion.
        """
        max_layers = max_layers or self.config.num_attention_layers

        # Convert tokens to embeddings (simplified)
        state = input_tokens
        if len(state.shape) == 1:
            state = state.reshape(1, -1)

        self.layer_history = []
        self.active_analyst_counts = []

        for layer_idx in range(max_layers):
            # Process layer
            state = self.process_layer(layer_idx, state)

            # Compute global temperature
            global_temp = self.compute_global_temperature()

            # Track layer statistics
            active_count = sum(1 for a in self.analysts[layer_idx] if a.is_active)
            layer_stats = {
                'layer': layer_idx,
                'active_analysts': active_count,
                'global_temperature': global_temp,
                'state_norm': np.linalg.norm(state)
            }
            self.layer_history.append(layer_stats)

            # Early stopping check
            if global_temp < self.config.early_stop_temp_threshold:
                print(f"Early stopping at layer {layer_idx} (global temp: {global_temp:.4f})")
                break

        # Determine number of output tokens based on state richness
        state_richness = np.std(state) * np.linalg.norm(state)
        num_output_tokens = min(
            self.config.max_tokens_per_pass,
            max(1, int(state_richness * 3))
        )

        return state, {
            'layers_processed': len(self.layer_history),
            'num_output_tokens': num_output_tokens,
            'final_global_temp': self.global_temperature,
            'layer_history': self.layer_history
        }

    def set_diffusion_layers_active(self, active_indices: List[int]):
        """User control: set which diffusion layers are active."""
        for i, layer in enumerate(self.diffusion_layers):
            layer.is_active = i in active_indices

    def set_constant_temperature(self, temp: float):
        """User control: set constant temperature (0 for determinism)."""
        for layer_analysts in self.analysts.values():
            for analyst in layer_analysts:
                analyst.temperature = temp
        self.ego_analyst.temperature = temp
        self.global_temperature = temp

    def provide_human_guidance(self, librarian_idx: int, attention_points: List[int]):
        """Human-guided training: point to where analysts should search."""
        if 0 <= librarian_idx < len(self.librarians):
            self.librarians[librarian_idx].set_attention_points(attention_points)

    def reset(self):
        """Reset system state for new inference."""
        # Reset all temperatures
        for layer_analysts in self.analysts.values():
            for analyst in layer_analysts:
                analyst.temperature = self.config.initial_local_temp
                analyst.is_active = True
                analyst.is_pruned = False
                analyst.facts_found = 0
                analyst.cumulative_similarity = 0.0
                analyst.resurrection_score = 0.0

        self.ego_analyst.temperature = self.config.initial_local_temp * 2
        self.global_temperature = self.config.initial_global_temp

        # Reset librarian fact temperatures
        for librarian in self.librarians:
            librarian.cluster.reset_temperatures()

        self.layer_history = []
        self.active_analyst_counts = []


# ============================================================================
# TRAINING CURRICULUM
# ============================================================================

class TrainingCurriculum:
    """
    Four-stage training curriculum:
    1. Train on stored facts with human guidance
    2. Remove guidance, self-directed learning
    3. Introduce new inputs with human labeling
    4. Synthetic data generation (math, etc.)
    """

    def __init__(self, system: LibrarianAnalystSystem):
        self.system = system
        self.current_stage = 1
        self.training_history: List[Dict] = []

    def stage1_guided_training(self, num_iterations: int = 100):
        """Stage 1: Train on facts with human guidance on where to search."""
        print("\n=== Stage 1: Guided Training on Stored Facts ===")

        for iteration in range(num_iterations):
            # Sample a fact from a librarian
            lib_idx = np.random.randint(len(self.system.librarians))
            librarian = self.system.librarians[lib_idx]
            fact_idx = np.random.randint(librarian.num_facts)

            # Provide human guidance: tell the system where to look
            self.system.provide_human_guidance(lib_idx, [fact_idx])

            # Create input from the fact (simulated)
            input_vec = librarian.facts[fact_idx] + np.random.randn(self.system.config.embedding_dim) * 0.1

            # Forward pass
            output, stats = self.system.forward(input_vec)

            # Simple loss: similarity to original fact
            target = librarian.facts[fact_idx]
            loss = 1.0 - np.dot(output.flatten()[:len(target)], target) / (
                np.linalg.norm(output) * np.linalg.norm(target) + 1e-8
            )

            self.training_history.append({
                'stage': 1,
                'iteration': iteration,
                'loss': loss,
                'layers_used': stats['layers_processed']
            })

            self.system.reset()

            if (iteration + 1) % 20 == 0:
                avg_loss = np.mean([h['loss'] for h in self.training_history[-20:]])
                print(f"  Iteration {iteration + 1}: Avg Loss = {avg_loss:.4f}")

    def stage2_unguided_training(self, num_iterations: int = 100):
        """Stage 2: Train without human guidance."""
        print("\n=== Stage 2: Unguided Training ===")

        for iteration in range(num_iterations):
            lib_idx = np.random.randint(len(self.system.librarians))
            librarian = self.system.librarians[lib_idx]
            fact_idx = np.random.randint(librarian.num_facts)

            # No guidance this time
            input_vec = librarian.facts[fact_idx] + np.random.randn(self.system.config.embedding_dim) * 0.1

            output, stats = self.system.forward(input_vec)

            target = librarian.facts[fact_idx]
            loss = 1.0 - np.dot(output.flatten()[:len(target)], target) / (
                np.linalg.norm(output) * np.linalg.norm(target) + 1e-8
            )

            self.training_history.append({
                'stage': 2,
                'iteration': iteration,
                'loss': loss,
                'layers_used': stats['layers_processed']
            })

            self.system.reset()

            if (iteration + 1) % 20 == 0:
                avg_loss = np.mean([h['loss'] for h in self.training_history[-20:]])
                print(f"  Iteration {iteration + 1}: Avg Loss = {avg_loss:.4f}")

    def stage3_new_inputs(self, num_iterations: int = 100):
        """Stage 3: Introduce new inputs not in librarians."""
        print("\n=== Stage 3: Training on New Inputs ===")

        for iteration in range(num_iterations):
            # Alternate between new and stored
            if iteration % 2 == 0:
                # New input
                input_vec = np.random.randn(self.system.config.embedding_dim)
                input_vec = input_vec / np.linalg.norm(input_vec)

                # Find closest librarian for guidance
                similarities = [lib.compute_similarity_to_librarian(input_vec)
                              for lib in self.system.librarians]
                best_lib_idx = np.argmax(similarities)
                self.system.provide_human_guidance(best_lib_idx, [0, 1, 2])
            else:
                # Stored fact
                lib_idx = np.random.randint(len(self.system.librarians))
                librarian = self.system.librarians[lib_idx]
                fact_idx = np.random.randint(librarian.num_facts)
                input_vec = librarian.facts[fact_idx]

            output, stats = self.system.forward(input_vec)

            # Loss is reconstruction + coherence
            loss = 1.0 - np.mean(np.abs(output))  # Simplified

            self.training_history.append({
                'stage': 3,
                'iteration': iteration,
                'loss': loss,
                'layers_used': stats['layers_processed']
            })

            self.system.reset()

            if (iteration + 1) % 20 == 0:
                avg_loss = np.mean([h['loss'] for h in self.training_history[-20:]])
                print(f"  Iteration {iteration + 1}: Avg Loss = {avg_loss:.4f}")

    def stage4_synthetic_data(self, num_iterations: int = 100):
        """Stage 4: Train on synthetic variations (e.g., math equations with swapped numbers)."""
        print("\n=== Stage 4: Synthetic Data Training ===")

        # Create a "template" fact
        template_lib = self.system.librarians[0]
        template_fact_idx = 0
        template_fact = template_lib.facts[template_fact_idx]

        for iteration in range(num_iterations):
            # Create variation of template
            variation_scale = np.random.uniform(0.8, 1.2)
            input_vec = template_fact * variation_scale
            input_vec = input_vec / np.linalg.norm(input_vec)

            # Guide to the template location
            self.system.provide_human_guidance(0, [template_fact_idx])

            output, stats = self.system.forward(input_vec)

            # Loss: should still recognize the template
            loss = 1.0 - np.dot(output.flatten()[:len(template_fact)], template_fact) / (
                np.linalg.norm(output) * np.linalg.norm(template_fact) + 1e-8
            )

            self.training_history.append({
                'stage': 4,
                'iteration': iteration,
                'loss': loss,
                'layers_used': stats['layers_processed']
            })

            self.system.reset()

            if (iteration + 1) % 20 == 0:
                avg_loss = np.mean([h['loss'] for h in self.training_history[-20:]])
                print(f"  Iteration {iteration + 1}: Avg Loss = {avg_loss:.4f}")


# ============================================================================
# VISUALIZATION
# ============================================================================

def visualize_system(system: LibrarianAnalystSystem, title: str = "Librarian-Analyst System"):
    """Visualize the system state and dynamics."""
    fig = plt.figure(figsize=(16, 12))
    gs = GridSpec(3, 3, figure=fig)

    # 1. Active analysts per layer
    ax1 = fig.add_subplot(gs[0, 0])
    if system.active_analyst_counts:
        ax1.plot(system.active_analyst_counts, 'b-', linewidth=2)
        ax1.set_xlabel('Processing Step')
        ax1.set_ylabel('Active Analysts')
        ax1.set_title('Analyst Pruning Dynamics')
        ax1.grid(True, alpha=0.3)

    # 2. Temperature distribution
    ax2 = fig.add_subplot(gs[0, 1])
    all_temps = []
    for layer_analysts in system.analysts.values():
        for analyst in layer_analysts:
            all_temps.append(analyst.temperature)
    if all_temps:
        ax2.hist(all_temps, bins=30, color='orange', alpha=0.7, edgecolor='black')
        ax2.axvline(system.global_temperature, color='red', linestyle='--',
                   label=f'Global: {system.global_temperature:.2f}')
        ax2.set_xlabel('Temperature')
        ax2.set_ylabel('Count')
        ax2.set_title('Analyst Temperature Distribution')
        ax2.legend()

    # 3. Layer statistics
    ax3 = fig.add_subplot(gs[0, 2])
    if system.layer_history:
        layers = [h['layer'] for h in system.layer_history]
        temps = [h['global_temperature'] for h in system.layer_history]
        active = [h['active_analysts'] for h in system.layer_history]

        ax3.plot(layers, temps, 'r-', label='Global Temp', linewidth=2)
        ax3_twin = ax3.twinx()
        ax3_twin.plot(layers, active, 'b-', label='Active Analysts', linewidth=2)

        ax3.set_xlabel('Layer')
        ax3.set_ylabel('Temperature', color='red')
        ax3_twin.set_ylabel('Active Analysts', color='blue')
        ax3.set_title('Layer-wise Dynamics')

    # 4. Librarian similarity matrix (sampled)
    ax4 = fig.add_subplot(gs[1, 0])
    sample_size = min(20, len(system.librarians))
    sim_matrix = np.zeros((sample_size, sample_size))
    for i in range(sample_size):
        for j in range(sample_size):
            sim_matrix[i, j] = system.librarians[i].compute_similarity_to_librarian(
                system.librarians[j].compressed_vector
            )
    im = ax4.imshow(sim_matrix, cmap='viridis')
    plt.colorbar(im, ax=ax4)
    ax4.set_title('Librarian Similarity Matrix')
    ax4.set_xlabel('Librarian Index')
    ax4.set_ylabel('Librarian Index')

    # 5. Architecture diagram
    ax5 = fig.add_subplot(gs[1, 1:])
    ax5.set_xlim(0, 10)
    ax5.set_ylim(0, 6)
    ax5.set_aspect('equal')
    ax5.axis('off')
    ax5.set_title('Architecture Overview', fontsize=14, fontweight='bold')

    # Draw components
    # Input
    rect1 = mpatches.FancyBboxPatch((0.5, 2.5), 1.5, 1, boxstyle="round,pad=0.05",
                                     facecolor='lightblue', edgecolor='black')
    ax5.add_patch(rect1)
    ax5.text(1.25, 3, 'Input\nTokens', ha='center', va='center', fontsize=9)

    # Self-Attention
    rect2 = mpatches.FancyBboxPatch((2.5, 2.5), 1.5, 1, boxstyle="round,pad=0.05",
                                     facecolor='lightgreen', edgecolor='black')
    ax5.add_patch(rect2)
    ax5.text(3.25, 3, 'Self\nAttention', ha='center', va='center', fontsize=9)

    # Cross-Attention (Analysts)
    rect3 = mpatches.FancyBboxPatch((4.5, 2), 2, 2, boxstyle="round,pad=0.05",
                                     facecolor='lightyellow', edgecolor='black')
    ax5.add_patch(rect3)
    ax5.text(5.5, 3, 'Cross-Attention\n(Analysts)', ha='center', va='center', fontsize=9)

    # Librarians
    rect4 = mpatches.FancyBboxPatch((4.5, 4.5), 2, 1, boxstyle="round,pad=0.05",
                                     facecolor='lightcoral', edgecolor='black')
    ax5.add_patch(rect4)
    ax5.text(5.5, 5, 'Librarians\n(Knowledge)', ha='center', va='center', fontsize=9)

    # Output
    rect5 = mpatches.FancyBboxPatch((7, 2.5), 1.5, 1, boxstyle="round,pad=0.05",
                                     facecolor='plum', edgecolor='black')
    ax5.add_patch(rect5)
    ax5.text(7.75, 3, 'Output\nState', ha='center', va='center', fontsize=9)

    # Arrows
    ax5.annotate('', xy=(2.4, 3), xytext=(2.1, 3),
                arrowprops=dict(arrowstyle='->', color='black'))
    ax5.annotate('', xy=(4.4, 3), xytext=(4.1, 3),
                arrowprops=dict(arrowstyle='->', color='black'))
    ax5.annotate('', xy=(6.9, 3), xytext=(6.6, 3),
                arrowprops=dict(arrowstyle='->', color='black'))
    ax5.annotate('', xy=(5.5, 4.4), xytext=(5.5, 4.1),
                arrowprops=dict(arrowstyle='<->', color='red'))

    # Temperature indicator
    ax5.text(5.5, 0.5, f'Global Temperature: {system.global_temperature:.3f}',
            ha='center', fontsize=11,
            bbox=dict(boxstyle='round', facecolor='wheat'))

    # 6. Facts retrieved histogram
    ax6 = fig.add_subplot(gs[2, 0])
    facts_found = []
    for layer_analysts in system.analysts.values():
        for analyst in layer_analysts:
            facts_found.append(analyst.facts_found)
    if facts_found and max(facts_found) > 0:
        ax6.hist(facts_found, bins=20, color='green', alpha=0.7, edgecolor='black')
        ax6.set_xlabel('Facts Retrieved')
        ax6.set_ylabel('Analyst Count')
        ax6.set_title('Retrieval Distribution')

    # 7. Cumulative similarity scores
    ax7 = fig.add_subplot(gs[2, 1])
    cum_sims = []
    for layer_analysts in system.analysts.values():
        for analyst in layer_analysts:
            if analyst.cumulative_similarity > 0:
                cum_sims.append(analyst.cumulative_similarity)
    if cum_sims:
        ax7.hist(cum_sims, bins=20, color='purple', alpha=0.7, edgecolor='black')
        ax7.set_xlabel('Cumulative Similarity')
        ax7.set_ylabel('Count')
        ax7.set_title('Analyst Contribution Scores')

    # 8. Master equation visualization
    ax8 = fig.add_subplot(gs[2, 2])
    ax8.axis('off')
    equation_text = (
        "Master Equation:\n\n"
        r"$s_{t+1} = \sum_i (W_i \cdot T_i \cdot s_t) + \epsilon$" + "\n\n"
        "Where:\n"
        r"$W_i$ = Analyst weights (learned)" + "\n"
        r"$T_i$ = Temperature (stochastic)" + "\n"
        r"$\epsilon$ = Diffusion noise" + "\n\n"
        "Thermodynamic Properties:\n"
        "• Energy: Fact temperatures\n"
        "• Entropy: Global temperature\n"
        "• Work: Information retrieval"
    )
    ax8.text(0.1, 0.9, equation_text, transform=ax8.transAxes, fontsize=10,
            verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    plt.tight_layout()
    return fig


def visualize_training(curriculum: TrainingCurriculum):
    """Visualize training progress across all stages."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    for stage in range(1, 5):
        ax = axes[(stage-1)//2, (stage-1)%2]
        stage_history = [h for h in curriculum.training_history if h['stage'] == stage]

        if stage_history:
            iterations = [h['iteration'] for h in stage_history]
            losses = [h['loss'] for h in stage_history]
            layers = [h['layers_used'] for h in stage_history]

            ax.plot(iterations, losses, 'b-', alpha=0.5, label='Loss')

            # Moving average
            window = 10
            if len(losses) >= window:
                moving_avg = np.convolve(losses, np.ones(window)/window, mode='valid')
                ax.plot(range(window-1, len(losses)), moving_avg, 'r-',
                       linewidth=2, label=f'Moving Avg ({window})')

            ax.set_xlabel('Iteration')
            ax.set_ylabel('Loss')
            ax.set_title(f'Stage {stage}: {"Guided" if stage==1 else "Unguided" if stage==2 else "New Inputs" if stage==3 else "Synthetic"}')
            ax.legend()
            ax.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig


# ============================================================================
# INTERACTIVE DEMO
# ============================================================================

def run_interactive_demo():
    """Run an interactive demonstration of the system."""
    print("=" * 70)
    print("LIBRARIAN-ANALYST ARCHITECTURE v2")
    print("Thermodynamic Neural Retrieval System")
    print("=" * 70)

    # Create configuration
    config = ArchitectureConfig(
        num_librarians=50,
        facts_per_librarian=256,
        num_attention_layers=15,
        cluster_depth=3,
        embedding_dim=64
    )

    print(f"\nConfiguration:")
    print(f"  Librarians: {config.num_librarians}")
    print(f"  Facts per librarian: {config.facts_per_librarian}")
    print(f"  Attention layers: {config.num_attention_layers}")
    print(f"  Embedding dimension: {config.embedding_dim}")
    print(f"  Total facts: {config.num_librarians * config.facts_per_librarian:,}")

    # Initialize system
    print("\n" + "-" * 50)
    system = LibrarianAnalystSystem(config)

    # Run inference with random input
    print("\n" + "-" * 50)
    print("Running inference with random input...")

    input_vec = np.random.randn(config.embedding_dim)
    input_vec = input_vec / np.linalg.norm(input_vec)

    output, stats = system.forward(input_vec)

    print(f"\nResults:")
    print(f"  Layers processed: {stats['layers_processed']}")
    print(f"  Output tokens: {stats['num_output_tokens']}")
    print(f"  Final global temperature: {stats['final_global_temp']:.4f}")

    # Show layer-by-layer statistics
    print("\n  Layer-wise statistics:")
    for layer_stat in stats['layer_history'][:10]:  # First 10 layers
        print(f"    Layer {layer_stat['layer']}: "
              f"Active={layer_stat['active_analysts']}, "
              f"Temp={layer_stat['global_temperature']:.3f}")

    # Test temperature control
    print("\n" + "-" * 50)
    print("Testing temperature controls...")

    system.reset()
    system.set_constant_temperature(0.0)
    output_deterministic, stats_det = system.forward(input_vec)
    print(f"  Deterministic mode (temp=0): {stats_det['layers_processed']} layers")

    system.reset()
    system.set_constant_temperature(2.0)
    output_creative, stats_creative = system.forward(input_vec)
    print(f"  Creative mode (temp=2): {stats_creative['layers_processed']} layers")

    # Test diffusion control
    print("\n" + "-" * 50)
    print("Testing diffusion layer control...")

    system.reset()
    system.set_diffusion_layers_active([])  # Disable all
    output_no_diff, stats_no_diff = system.forward(input_vec)
    print(f"  No diffusion: {stats_no_diff['final_global_temp']:.4f} final temp")

    system.reset()
    system.set_diffusion_layers_active(list(range(config.num_diffusion_layers)))  # Enable all
    output_full_diff, stats_full_diff = system.forward(input_vec)
    print(f"  Full diffusion: {stats_full_diff['final_global_temp']:.4f} final temp")

    # Visualize
    print("\n" + "-" * 50)
    print("Generating visualization...")

    system.reset()
    system.forward(input_vec)  # Run again for fresh stats

    fig1 = visualize_system(system, "Librarian-Analyst System State")
    fig1.savefig('/home/user/Claude_freespace/librarian_analyst_system.png', dpi=150, bbox_inches='tight')
    print("  Saved: librarian_analyst_system.png")

    # Run training curriculum (abbreviated)
    print("\n" + "-" * 50)
    print("Running abbreviated training curriculum...")

    system.reset()
    curriculum = TrainingCurriculum(system)
    curriculum.stage1_guided_training(num_iterations=50)
    curriculum.stage2_unguided_training(num_iterations=50)

    fig2 = visualize_training(curriculum)
    fig2.savefig('/home/user/Claude_freespace/librarian_analyst_training.png', dpi=150, bbox_inches='tight')
    print("  Saved: librarian_analyst_training.png")

    # Summary statistics
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    total_analysts = sum(len(a) for a in system.analysts.values())
    active_analysts = sum(1 for layer_analysts in system.analysts.values()
                         for a in layer_analysts if a.is_active)
    pruned_analysts = total_analysts - active_analysts

    print(f"Total analysts: {total_analysts}")
    print(f"Active analysts: {active_analysts} ({100*active_analysts/total_analysts:.1f}%)")
    print(f"Pruned analysts: {pruned_analysts} ({100*pruned_analysts/total_analysts:.1f}%)")
    print(f"Global temperature: {system.global_temperature:.4f}")
    print(f"Resurrection threshold: {system.compute_resurrection_threshold():.4f}")

    plt.show()

    return system, curriculum


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def np_softmax(x, axis=-1):
    """Numerically stable softmax."""
    exp_x = np.exp(x - np.max(x, axis=axis, keepdims=True))
    return exp_x / np.sum(exp_x, axis=axis, keepdims=True)

# Monkey-patch numpy with softmax
np.softmax = np_softmax


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    system, curriculum = run_interactive_demo()
